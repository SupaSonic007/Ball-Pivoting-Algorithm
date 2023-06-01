from typing import Any

import numpy as np
from point import Point

class Edge:

    def __init__(self, p1:Point, p2:Point) -> None:
        """
        Initialise the edge with two points
        :param p1: The first point
        :param p2: The second point
        """
        self.p1 = p1
        self.p2 = p2
        self.edge = (p1, p2)

    def get_points(self) -> tuple:
        """
        Return the points for each edge
        :return: A tuple containing the two points connected as the edge
        """
        return (self.p1, self.p2)
    
    def find_third_point(self, point_cloud: np.array, radius: float) -> Point:
        """
        Find the third point of the triangle by pivoting the ball around the edge
        :param point_cloud: The point cloud to find the third point in
        :param radius: The radius to search for the third point
        :return: The third point of the triangle
        """
        
        # Get neighbours from p1 and p2, then center of edge
        p1_neighbours_points, p1_neighbours_distances = self.p1.find_neighbouring_vertices_with_distance(point_cloud, radius)
        p2_neighbours_points, p2_neighbours_distances = self.p2.find_neighbouring_vertices_with_distance(point_cloud, radius)

        # Get box betweek p1 & p2 & radius (./vennsquare.png)
        # Get points in box
        
        

        return
    
    def __call__(self, *args: Any, **kwds: Any) -> tuple:
        return self.get_points()