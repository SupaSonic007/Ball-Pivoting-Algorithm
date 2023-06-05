import numpy as np # numpy faster in math operations
import open3d as o3d
import threading

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

    def __init__(self, radius: float, point_cloud: np.ndarray= None, file_location: str= None, iterations= None, original_point_cloud= None) -> None:
        """
        Initializes the Ball Pivoting Algorithm with the given point cloud and radius.
        :param point_cloud: The point cloud to be interpolated.
        :param radius: The radius of the ball used for pivoting.
        :param file_location: The location of the object file.
        :param iterations: The number of iterations to run the algorithm for (Choose a specific amount for testing purposes).
        :param original_point_cloud: The original point cloud (Used for indexing purposes).
        """
        if file_location and type(point_cloud) == None:
            self.open_point_cloud(file_location)
        else: 
            self.point_cloud = point_cloud
        self.file_location = file_location
        self.radius = radius
        self.iterations = iterations
        self.original_point_cloud = original_point_cloud
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
        i = 0
        while len(distances) == 0: 
            i += 1
            if i >= len(self.point_cloud): self.write_to_file(); quit()
            first_point = self.point_cloud[i]
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
        if type(self.original_point_cloud) == None:
            return Face((first_point, second_point, third_point), (first_edge, second_edge, third_edge), (np.where(self.point_cloud == first_point)[0][0], np.where(self.point_cloud == second_point)[0][0], np.where(self.point_cloud == third_point)[0][0]))
        else:
            return Face((first_point, second_point, third_point), (first_edge, second_edge, third_edge), (np.where(self.original_point_cloud == first_point)[0][0], np.where(self.original_point_cloud == second_point)[0][0], np.where(self.original_point_cloud == third_point)[0][0]))
    
    def pivot_ball(self, edge:Edge):
        """
        Pivots the ball around the given edge until it touches another point.
        :param edge: The edge to pivot the ball around.
        :return: The next triangle formed by the ball pivoting around the edge.
        """
        
        # Find third point of triangle
        third_point = edge.find_third_point(self.point_cloud, self.radius, self.faces)

        second_edge = Edge(edge.p1, third_point)
        third_edge = Edge(edge.p2, third_point)
        self.edges.append(second_edge)
        self.edges.append(third_edge)

        self.edges = list(set(self.edges))
        
        # np.where(xxx)[0][0] gets the index of the point in the point cloud for use in saving to file later
        if type(self.original_point_cloud) == None:
            return Face((edge.p1, edge.p2, third_point), (edge, second_edge, third_edge), (np.where(self.point_cloud == edge.p1)[0][0], np.where(self.point_cloud == edge.p2)[0][0], np.where(self.point_cloud == third_point)[0][0]))
        else:
            return Face((edge.p1, edge.p2, third_point), (edge, second_edge, third_edge), (np.where(self.original_point_cloud == edge.p1)[0][0], np.where(self.original_point_cloud == edge.p2)[0][0], np.where(self.original_point_cloud == third_point)[0][0]))

    def write_to_file(self, file_location:str=None) -> None:
        """
        Writes the triangle mesh to an object file.
        :param file_location: The location of the object file.
        """

        if file_location is None:
            file_location = self.file_location
        edited_file_location = file_location.split('.')
        edited_file_location[-2] += '_edited'

        with open(".".join(edited_file_location), 'r+') as f:
            if not f'# {file_location}' in f.read():
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
        with open(".".join(edited_file_location), 'r+') as f:
            if not f'# {file_location}' in f.read():
                f.write(f"# {file_location}\n")

            for point in self.point_cloud:
                f.write(f"v {point.x} {point.y} {point.z}\n")

        return
    
    def init_file(self):
        """
        Initialises the files for the point cloud and the mesh
        """
        edited_file = self.file_location.split('.')[0] + '_edited.obj'
        point_cloud = self.file_location.split('.')[0] + '_point_cloud.obj'
        with open(edited_file, "w"):
            pass
        with open(point_cloud, "w"):
            pass

        return
    
    def points_left(self) -> bool:
        """
        Checks if there are any edges that don't have 2 connections.
        :return: True if there are points left, False otherwise.
        """

        # ! Not implemented yet. Don't worry about this
        
        for edge in self.edges:
            if edge.connections < 2:
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
        for i in range(self.iterations): # Only run x iterations to test, still slow but don't worry about that
            
            face = self.pivot_ball(edge)
            self.faces.append(face)
            
            edge = face.get_new_edge() # <---- To understand how this works, please check face.py (It's quite simple but important)
            k = 0
            while edge == None:
                if k > len(self.faces): self.write_to_file(); quit()
                face = self.faces[k]
                edge = face.get_new_edge()
                k += 1

        self.write_to_file()

        return np.array([])

def main(radius, shards=4):

    bpa = BallPivotingAlgorithm(0.003, file_location='stanford-bunny.obj')
    bpa.open_point_cloud('stanford-bunny.obj')
    bpa.init_file()
    point_cloud = bpa.point_cloud

    # Split the point cloud into shards
    shard_size = len(point_cloud)/shards
    shards_list = [point_cloud[i:i+int(np.floor(shard_size))] for i in range(0, len(point_cloud), int(np.floor(shard_size)))]

    # Keep track of each algorithm
    algorithm_threads = []
    
    for i in range(shards):
        bpa_shard = BallPivotingAlgorithm(0.0025, point_cloud=shards_list[i], iterations=5, file_location='stanford-bunny.obj', original_point_cloud=point_cloud)
        algorithm_threads.append(threading.Thread(target=bpa_shard.run))
        algorithm_threads[i].start()

    for thread in algorithm_threads:
        thread.join()
    
    if len(shards_list) > shards:
        # Run last shard to get the remaining points
        bpa_shard = BallPivotingAlgorithm(0.0025, point_cloud=shards_list[-1], iterations=5, file_location='stanford-bunny.obj', original_point_cloud=point_cloud)
        bpa_shard.run()


if __name__ == '__main__':
    main(0.0025, 5)
