import numpy as np

def cosine_rule(a:float, b:float, c:float) -> float:
        """
        Calculate the angle 'C' of a triangle using the cosine rule
        :param a: The length of side 'a'
        :param b: The length of side 'b'
        :param c: The length of side 'c'
        :return: The angle 'C' of the triangle
        """
        angleC = np.arccos(
            np.divide(
                np.square(a) + np.square(b) - np.square(c),
                np.multiply(2, np.multiply(a, b))
            )
        )

        return angleC

def sine_rule_for_side(a:float, A:float, C:float) -> float:
    """
    Calculate the length of side 'b' of a triangle using the sine rule
    :param a: The length of side 'a'
    :param A: The angle 'A' of the triangle
    :param C: The angle 'C' of the triangle
    :return: The length of side 'c'
    """
    
    c = np.divide(
        np.multiply(
            a,
            np.sin(C)
        ),
        np.sin(A)
    )

    return c