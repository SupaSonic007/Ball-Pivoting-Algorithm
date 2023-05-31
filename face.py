from typing import Any
import numpy as np

class Face:

    def __init__(self, p1, p2, p3) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def __call__(self, *args: Any, **kwds: Any) -> np.array:
        return np.array(self.p1, self.p2, self.p3)