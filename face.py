from typing import Any

import numpy as np

from edge import Edge


class Face:
    """
    A face is a triangle made up of three points.
    """

    def __init__(self, points: tuple, edges: tuple, indexes_for_points: tuple) -> None:
        """
        Initialise the face with three points & edges
        :param points: The three points
        :param edges: The three edges
        """

        self.p1 = points[0]
        self.p2 = points[1]
        self.p3 = points[2]

        self.p1_index = indexes_for_points[0]
        self.p2_index = indexes_for_points[1]
        self.p3_index = indexes_for_points[2]

        self.edge1 = edges[0]
        self.edge2 = edges[1]
        self.edge3 = edges[2]

        # Add connections to edges (There should be a maximum of 2 connections per edge so as not to overlap faces)
        self.edge1.connections += 1
        self.edge2.connections += 1
        self.edge3.connections += 1

    def __call__(self, *args: Any, **kwds: Any) -> np.array:
        return self.get_points

    def __repr__(self) -> str:
        return f"<Face {self.edge1, self.edge2, self.edge3}>"

    def get_points(self):
        """
        Return the points for each face as an array
        :return: An array containing the three points connected as the face
        """
        return np.array([self.p1, self.p2, self.p3])

    def get_edges(self):
        """
        Return the edges for each face as an array
        :return: An array containing the three edges connected as the face
        """
        return np.array([self.edge1, self.edge2, self.edge3])

    def get_new_edge(self) -> Edge:
        """
        Get a new edge to start from to build a new face
        :return: The new edge for the new face
        """
        # If an edge has 2 connections, don't use it because there will be overlap
        edge = self.edge3
        if edge.connections >= 2:
            edge = self.edge2
        if edge.connections >= 2:
            edge = self.edge1
        if edge.connections >= 2:
            edge = None
        return edge
