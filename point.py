from __future__ import annotations
from typing import Any
import numpy as np


class Point:

    def __init__(self, location: list, x: float = None, y: float = None, z: float = None) -> None:
        if x and y and z:
            self.x = x
            self.y = y
            self.z = z
            self.location = (x, y, z)
        else:
            self.x = location[0]
            self.y = location[1]
            self.z = location[2]
            self.location = location

    def __call__(self, *args: Any, **kwds: Any) -> tuple:
        return self.location

    def __repr__(self) -> str:
        return f"<Point {self.x, self.y, self.z}>"

    def find_neighbouring_vertices(self, point_cloud: np.array, radius: float) -> np.array:
        """
        Find the neighbouring vertices within a certain radius
        :param point_cloud: The point cloud to find neighbours within
        :param radius: The radius to search for neighbours
        :return: An array of neighbouring points in the radius
        """

        neighbours = []

        for point in point_cloud:
            point: Point
            if point == self:
                continue
            distance = self.distance_to_point(point)
            if distance < radius:
                neighbours.append(point)
                print(self, point)

        return np.array(neighbours)

    def find_neighbouring_vertices_with_distance(self, point_cloud: np.array, radius: float) -> np.array:
        """
        Find the neighbouring vertices within a certain radius
        :param point_cloud: The point cloud to find neighbours within
        :param radius: The radius to search for neighbours
        :return: An array of neighbouring points in the radius with distances
        """

        neighbours = []
        distances = []

        for point in point_cloud:
            point: Point
            if point == self:
                continue
            distance = self.distance_to_point(point)
            if distance < radius:
                neighbours.append(point)
                distances.append(distance)

        return np.array(neighbours), np.array(distances)

    def distance_to_point(self, point) -> float:
        """
        Find distance of a point in relation to this point
        :param point: Point to compare location to
        :return: distance to 
        """

        # √((a2-a1)^2 + (b2-b1)^2 + (c2-c1)^2)

        x = np.power(point.x-self.x, 2)
        y = np.power(point.y-self.y, 2)
        z = np.power(point.z-self.z, 2)
        distance = np.sqrt(
            np.add(
                np.add(
                    x, y
                ),
                z
            )
        )

        return float(distance)

    def get_closest_point(self, points: np.array, distances: np.array, exclude: list = None) -> Point:
        """
        Get the vertex closest to this vertex
        :param points: NumPy Array of Point objects -> return the closest
        :param distances: NumPy Array of floating point numbers to find the minimum
        :return: Point object with the closest relative position
        """

        closest_index = np.where(distances == min(distances))
        closest = points[closest_index]

        return closest[0]

    def get_location(self) -> tuple:
        """
        Get the location of the point
        :return: The location of the point
        """
        return self.location