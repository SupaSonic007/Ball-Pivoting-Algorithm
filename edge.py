from typing import Any

import numpy as np
from point import Point
import trigonometry as trig

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
        
        points_and_distances = []

        for point in point_cloud:
            point: Point
            if point == self.p1 or point == self.p2: continue
            # Get angle from cosine rule and then find distance using sine rule
            a = self.p1.distance_to_point(point)
            b = self.p2.distance_to_point(point)
            c = self.p1.distance_to_point(self.p2)
            angleC = trig.cosine_rule(a, b, c)
            angleA = trig.cosine_rule(b, c, a)

            distance_to_third_point = trig.sine_rule_for_side(a, angleA, angleC)
            
            if not distance_to_third_point <= radius: continue

            points_and_distances.append((point, distance_to_third_point))
        
        # Sort the points by distance
        closest = points_and_distances.sort(key=lambda x: x[1])[0]
        
        return closest[0]

    def __call__(self, *args: Any, **kwds: Any) -> tuple:
        return self.get_points()