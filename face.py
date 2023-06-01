from typing import Any

import numpy as np


class Face:
    """
    A face is a triangle made up of three points.
    """
    
    def __init__(self, p1, p2, p3) -> None:
        """
        Initialise the face with three points
        :param p1: The first point
        :param p2: The second point
        :param p3: The third point
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __call__(self, *args: Any, **kwds: Any) -> np.array:
        return self.get_points

    def get_points(self):
        """
        Return the points for each face as an array
        :return: An array containing the three points connected as the face
        """
        return np.array(self.p1, self.p2, self.p3)