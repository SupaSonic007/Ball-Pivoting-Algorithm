import numpy as np # numpy faster in math operations
import open3d as o3d

from edge import Edge
from face import Face
from point import Point
from visualiser import Visualiser


class BallPivotingAlgorithm:
    """
    An algorithm for reconstructing surfaces of a mesh.
    """

    faces = []
    edges = []

    def __init__(self, radius: float, point_cloud: np.ndarray = None, file_location: str = None) -> None:
        """
        Initializes the Ball Pivoting Algorithm with the given point cloud and radius.
        :param point_cloud: The point cloud to be interpolated.
        :param radius: The radius of the ball used for pivoting.
        """
        self.point_cloud = point_cloud or np.ndarray([])
        if file_location:
            self.open_point_cloud(file_location)
            self.file_location = file_location
        self.radius = radius
        return

    def open_point_cloud(self, file_location: str) -> None:
        """
        Opens an object file, filtering out the points in the point cloud
        :param file_location: The location of the object file
        """

        file_list = ['obj']
        if file_location.split('.')[-1] not in file_list:
            raise ValueError(f"Only able to read object data of types {file_list}")

        with open(file_location, 'r') as f:
            # Initialise points to be added to numpy array
            points = []

            for line in f.readlines():
                # There must be text in the line and it must be a vertex
                if not len(line) > 3:
                    continue
                # Segments of string
                segments = line.split()

                if segments[0] != 'v': continue

                points.append([
                        float(segments[1]),
                        float(segments[2]),
                        float(segments[3])
                    ])

            self.point_cloud = np.array([Point(point) for point in points])

        return

    def find_seed_triangle(self) -> Face:
        """
        Finds a seed triangle to start the algorithm.
        :return: A seed triangle.
        """

        first_point = self.point_cloud[0]

        # Find second point by distance
        neighbours, distances = first_point.find_neighbouring_vertices_with_distance(self.point_cloud, self.radius)
        second_point = first_point.get_closest_point(neighbours, distances)

        first_edge = Edge(first_point, second_point)
        self.edges.append(first_edge)

        # Find third point through shared neighbour along edge (Cylindrical space)
        third_point = first_edge.find_third_point(self.point_cloud, self.radius, self.faces)
        
        second_edge = Edge(second_point, third_point)
        
        third_edge = Edge(third_point, first_point)

        self.edges.append(second_edge)
        self.edges.append(third_edge)

        # np.where(xxx)[0][0] gets the index of the point in the point cloud for use in saving to file later
        seed_triangle = Face((first_point, second_point, third_point), (first_edge, second_edge, third_edge), (np.where(self.point_cloud == first_point)[0][0], np.where(self.point_cloud == second_point)[0][0], np.where(self.point_cloud == third_point)[0][0]))
        self.faces.append(seed_triangle)

        return seed_triangle

    def pivot_ball(self, edge:Edge):
        """
        Pivots the ball around the given edge until it touches another point.
        :param edge: The edge to pivot the ball around.
        :return: The next triangle formed by the ball pivoting around the edge.
        """
        
        # Find third point of triangle
        third_point = edge.find_third_point(self.point_cloud, self.radius, self.faces)

        edge_1_exists = False
        edge_2_exists = False
        second_edge = None
        third_edge = None

        for self_edge in self.edges:
            # Check if the other 2 edges exist in self.edges, if not, add them
            if edge_1_exists and edge_2_exists:
                break
            elif edge.p1 in self_edge.get_points() and third_point in self_edge.get_points():
                edge_1_exists = True
                second_edge = self_edge
            elif edge.p2 in self_edge.get_points() and third_point in self_edge.get_points():
                edge_2_exists = True
                third_edge = self_edge
            else:
                second_edge = Edge(edge.p1, third_point)
                third_edge = Edge(edge.p2, third_point)
                self.edges.append(second_edge)
                self.edges.append(third_edge)
            
        # np.where(xxx)[0][0] gets the index of the point in the point cloud for use in saving to file later
        return Face((edge.p1, edge.p2, third_point), (edge, second_edge, third_edge), (np.where(self.point_cloud == edge.p1)[0][0], np.where(self.point_cloud == edge.p2)[0][0], np.where(self.point_cloud == third_point)[0][0]))

    def write_to_file(self, file_location:str=None) -> None:
        """
        Writes the triangle mesh to an object file.
        :param file_location: The location of the object file.
        """

        if file_location is None:
            file_location = self.file_location
        edited_file_location = file_location.split('.')
        edited_file_location[-2] += '_edited'

        with open(".".join(edited_file_location), 'w') as f:
            f.write(f"# {file_location}\n")

            for point in self.point_cloud:
                f.write(f"v {point.x} {point.y} {point.z}\n")
            
            f.write(f"\n")

            for face in self.faces:
                f.write(f"f {face.p1_index+1} {face.p2_index+1} {face.p3_index+1}\n")
        
        # Create point cloud file
        if file_location is None:
            file_location = self.file_location
        edited_file_location = file_location.split('.')
        edited_file_location[-2] += '_point_cloud'
        with open(".".join(edited_file_location), 'w') as f:
            f.write(f"# {file_location}\n")

            for point in self.point_cloud:
                f.write(f"v {point.x} {point.y} {point.z}\n")

        return
    
    def points_left(self) -> bool:
        """
        Checks if there are any edges that don't have 2 connections.
        :return: True if there are points left, False otherwise.
        """

        # ! Not implemented yet. Don't worry about this
        
        # variables
        points_left = False

        for edge in self.edges:
            if edge.connections < 2:
                points_left = True
                return True
            
        return False


    def run(self):
        """
        Runs the Ball Pivoting Algorithm to compute a triangle mesh interpolating the point cloud.
        :return: A triangle mesh interpolating the point cloud.
        """
        seed_triangle = self.find_seed_triangle()
        self.faces.append(seed_triangle)
        edge = seed_triangle.get_new_edge()
        for i in range(10): # Only run 10 iterations to test, still slow but don't worry about that
            
            face = self.pivot_ball(edge)
            self.faces.append(face)
            
            edge = face.get_new_edge() # <---- To understand how this works, please check face.py (It's quite simple but important)
            print(i+1)
            while edge == None:
                k = 0
                if k > len(self.faces): break
                face = self.faces[k]
                edge = face.get_new_edge()
                k += 1

        self.write_to_file()

        return np.array([])

def main():

    bpa = BallPivotingAlgorithm(0.003, file_location='stanford-bunny.obj')
    bpa.run()

    pass


if __name__ == '__main__':
    main()
