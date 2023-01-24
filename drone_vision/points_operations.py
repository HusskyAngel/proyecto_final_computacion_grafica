from typing import List, Tuple
from math import sqrt, pi

from point import point

EPSILON = 0.00001
ONE_RADIAN_IN_GRADES = 180/pi
COLLINEAR_ORIENTATION = 0
CLOCKWISE_ORIENTATION = 1
COUNTERCLOCKWISE_ORIENTATION = 2


def vector_norm(vector: point, origin: point = point(0, 0, 0)):
    """
    Calculates the norm of 'vector' to 'origin'.
    """
    norm = sqrt(((vector.x - origin.x) ** 2) +
                ((vector.y - origin.y) ** 2))
    return norm


def get_orientation(A: point, B: point, C: point):
    """
    Determines the orientation of the points in the order A->B->C, returning one of the 
    following results:
    - 0 : the points were collinear.
    - 1 : the points were clockwise.
    - 2 : the points were counterclockwise.
    """

    a1 = A.y - B.y
    b1 = B.x - A.x

    a2 = B.y - C.y
    b2 = C.x - B.x

    val = a2*b1 - a1*b2

    # Collinear points.
    if (abs(val) < EPSILON):
        return COLLINEAR_ORIENTATION

    # Clockwise points.
    if val > 0.0:
        return CLOCKWISE_ORIENTATION

    return COUNTERCLOCKWISE_ORIENTATION
