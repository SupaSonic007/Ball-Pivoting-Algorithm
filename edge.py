from typing import Any

import numpy as np

import trigonometry as trig
from point import Point


class Edge:

    def __init__(self, p1: Point, p2: Point) -> None:
        """
        Initialise the edge with two points
        :param p1: The first point
        :param p2: The second point
        """

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
        if self.connections >= 2:
            return None

        points_and_distances = list()

        for point in point_cloud:
            if point == self.p1 or point == self.p2:
                continue

            # Get angle from cosine rule
            a = self.p1.distance_to_point(point)
            b = self.p2.distance_to_point(point)
            c = self.p1.distance_to_point(self.p2)
            angleC = trig.cosine_rule(a, b, c)

            if self.check_overlap((self.p1, self.p2), point, faces):
                continue
            points_and_distances.append((point, angleC))

        # Sort the points by distance (the larger the angle, the closer the point is to the middle of the edge)
        points_and_distances.sort(key=lambda x: x[1], reverse=True)

        if len(points_and_distances) == 0:
            return None

        self.connections += 1

        return points_and_distances[0][0]

    def check_overlap(self, edge: tuple, point: Point, faces: list) -> bool:
        """
        Check if the face already exists in the list of faces
        :param edge: The edge to check for overlaps
        :param point: The point to check against
        :param faces: The faces to check for overlaps
        :return: Whether the edge overlaps with any other edges
        """

        if len(faces) == 0:
            return False

        for face in faces:
            points = face.get_points()
            # if all points are in the face, then it's the same face
            if set([self.p1, self.p2, point]).issubset(points):
                return True

        # Check if previous face uses 2 of the same points
        for edge in faces[-1].get_edges():
            points_for_edge = edge.get_points()
            if set(points_for_edge).issubset([self.p1, point]):
                return True
            if set(points_for_edge).issubset([self.p2, point]):
                return True

        # Calculate Normals For original triangle and new triangle to see if there is an overlap
       
        points = faces[-1].get_points()
       
        vector1 = [points[2].x - points[0].x, points[2].y -
              points[0].y, points[2].z - points[0].z]
       
        vector2 = [points[1].x - points[0].x, points[1].y -
              points[0].y, points[1].z - points[0].z]

        # Cross product the two vectors to get the normal of the triangle
        triangle_normal = np.cross(vector1, vector2)

        plane_normal = np.cross(vector2, triangle_normal)
        # Vertical line on edge, 90 degrees to triangle

        # Check if point is on same side of plane
        vector3 = [point.x - points[0].x, point.y -
              points[0].y, point.z - points[0].z]

        # Method of checking vector normals from Lotemn102's Ball-Pivoting-Algorithm implementation @ github.com/Lotemn102/Ball-Pivoting-Algorithm/
        return not np.sign(np.dot(plane_normal, vector1)) == np.sign(np.dot(plane_normal, vector3))
