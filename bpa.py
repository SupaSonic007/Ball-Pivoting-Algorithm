import numpy as np
# Using numpy as it is faster for mathematical operations
from edge import Edge
from face import Face
from point import Point

class BallPivotingAlgorithm:

    def __init__(self, radius:float, point_cloud:np.ndarray=None, file_location:str=None) -> None:
        """
        Initializes the Ball Pivoting Algorithm with the given point cloud and radius.
        :param point_cloud: The point cloud to be interpolated.
        :param radius: The radius of the ball used for pivoting.
        """
        self.point_cloud = point_cloud or np.ndarray([])
        if file_location: self.open_point_cloud(file_location)
        self.radius = radius
        return
    
    def open_point_cloud(self, file_location:str) -> None:
        """
        Opens an object file, filtering out the points in the point cloud
        """

        file_list = ['obj']
        if file_location.split('.')[-1] not in file_list: raise(ValueError(f"Only able to read object data of types {file_list}"))

        with open(file_location, 'r') as f:
            # Initialise points to be added to numpy array
            points = []

            for line in f.readlines():
                # There must be text in the line and it must be a vertex
                if not len(line) > 3: continue
                if not line.split()[0] == 'v': continue

                points.append(line.split()[1::])
            self.point_cloud = np.array([Point(point) for point in points])

        return

    def find_seed_triangle(self) -> np.array:
        """
        Finds a seed triangle to start the algorithm.
        :return: A seed triangle.
        """

        return

    def pivot_ball(self, edge):
        """
        Pivots the ball around the given edge until it touches another point.
        :param edge: The edge to pivot the ball around.
        :return: The next triangle formed by the ball pivoting around the edge.
        """
        
        return

    def run(self):
        """
        Runs the Ball Pivoting Algorithm to compute a triangle mesh interpolating the point cloud.
        :return: A triangle mesh interpolating the point cloud.
        """
        
        return np.array([])

def main():

    bpa = BallPivotingAlgorithm(0.005, file_location='./stanford-bunny.obj')
    bpa.run()

    pass

if __name__ == '__main__':
    main()