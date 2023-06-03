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
        
        points = [p1, p2]
        points.sort(key=lambda x: (x.x, x.y, x.z))
        
        p1 = points[0]
        p2 = points[1]

        self.p1 = p1
        self.p2 = p2
        self.edge = (p1, p2)
        # The number of times this edge has been checked for a third point (Can only connect to 2 points)
        self.connections = 0

    def __call__(self, *args: Any, **kwds: Any) -> tuple:
        return self.get_points()
    
    def __repr__(self) -> str:
        return f"<Edge {self.p1, self.p2}>"

    def get_points(self) -> tuple:
        """
        Return the points for each edge
        :return: A tuple containing the two points connected as the edge
        """

        return (self.p1, self.p2)
    
    def find_third_point(self, point_cloud: np.array, radius: float, faces: list) -> Point:
        """
        Find the third point of the triangle by pivoting the ball around the edge
        :param point_cloud: The point cloud to find the third point in
        :param radius: The radius to search for the third point
        :return: The third point of the triangle
        """
        if self.connections >= 2: return None

        points_and_distances = list()

        for point in point_cloud:
            point: Point
            if point == self.p1 or point == self.p2: continue
            
            # Get angle from cosine rule
            a = self.p1.distance_to_point(point)
            b = self.p2.distance_to_point(point)
            c = self.p1.distance_to_point(self.p2)
            angleC = trig.cosine_rule(a, b, c)

            if self.check_overlap((self.p1, self.p2), point, faces): continue
            points_and_distances.append((point, angleC))
        
        # Sort the points by distance (the larger the angle, the closer the point is to the middle of the edge)
        points_and_distances.sort(key=lambda x: x[1], reverse=True)
        
        if len(points_and_distances) == 0: self.connections += 1
        
        return points_and_distances[0][0]

    def check_overlap(self, edge:tuple, point:Point, faces:list) -> bool:
        """
        Check if the edge overlaps with any other edges
        :param edge: The edge to check for overlaps
        :param point: The point to check against
        :param faces: The faces to check for overlaps
        :return: Whether the edge overlaps with any other edges
        """
        from face import Face

        for face in faces:
            face:Face
            if self.p1 in face.get_points() and self.p2 in face.get_points() and point in face.get_points():
                return True
            
                
        return False
