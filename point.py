from typing import Any
import numpy as np

class Point:

    def __init__(self, location: list, x:float=None, y:float=None, z:float=None) -> None:
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
        return (self.x, self.y, self.z)
    
    def find_neighbouring_vertices(self, point_cloud:np.array, radius: float) -> np.array:
        """
        Find the neighbouring vertices within a certain radius
        """
        # TODO
        for point in point_cloud:
            pass
        neighbours = None

        return neighbours
    
    def __repr__(self) -> str:
        return f"<Point {self.x, self.y, self.z}>"