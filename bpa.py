import numpy as np # numpy faster in math operations
import open3d as o3d

from edge import Edge
from face import Face
from point import Point
from visualiser import Visualiser


class BallPivotingAlgorithm:

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

    def find_seed_triangle(self) -> np.array:
        """
        Finds a seed triangle to start the algorithm.
        :return: A seed triangle.
        """

        first_point = self.point_cloud[0]
        first_point:Point

        # Find second point by distance
        neighbours, distances = first_point.find_neighbouring_vertices_with_distance(self.point_cloud, self.radius)
        second_point = first_point.get_closest_point(neighbours, distances)
        second_point:Point

        first_edge = Edge(first_point, second_point)
        first_edge:Edge

        # Find third point through shared neighbour along edge (Cylindrical space)
        third_point = first_edge.find_third_point(self.point_cloud, self.radius)

        # First point -> Second point through closest neighbour
        # distance: +/-(p1 -> p2 * radius) to get bounding box (above and below), find third point between
        # If no point found, move on, no face/triangle

        return
    
    def find_third_point(self, point1:Point, point2:Point) -> Point:
        pass

    def pivot_ball(self, edge:Edge):
        """
        Pivots the ball around the given edge until it touches another point.
        :param edge: The edge to pivot the ball around.
        :return: The next triangle formed by the ball pivoting around the edge.
        """
        
        # Find third point of triangle
        third_point = edge.find_third_point(self.point_cloud, self.radius)

        return

    def run(self):
        """
        Runs the Ball Pivoting Algorithm to compute a triangle mesh interpolating the point cloud.
        :return: A triangle mesh interpolating the point cloud.
        """
        self.find_seed_triangle()
        while self.points_left():
            pass

        return np.array([])


def main():

    bpa = BallPivotingAlgorithm(0.003, file_location='stanford-bunny.obj')
    bpa.run()

    pass


if __name__ == '__main__':
    main()
