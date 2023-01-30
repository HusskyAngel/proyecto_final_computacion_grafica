from typing import List, Tuple
from math import pi, acos

from drone_vision.point import point
from drone_vision.points_operations import get_orientation, vector_norm

EPSILON = 0.00001
ONE_RADIAN_IN_GRADES = 180/pi
COLLINEAR_ORIENTATION = 0
CLOCKWISE_ORIENTATION = 1
COUNTERCLOCKWISE_ORIENTATION = 2


def get_point_inside_line_by_y_coordinate(A: point, B: point, y: float) -> point:
    """
    Calculates the point inside line by specifying 'y' coordinate.
    """

    # m = -a1/b1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)

    if (abs(b1) < EPSILON):
        # A.x == B.x
        return point(A.x, y, 0)

    if(abs(a1) < EPSILON):
        # A.y == B.y
        # The answer could be any point inside line AB
        return point(A.x, y, 0)

    x = -(b1*y + c1)/a1

    return point(x, y, 0)


def project_point_on_line(A: point, B: point, C: point):
    """
    Generates an orthogonal projection of point C in line defined by points
    A and B.
    """

    if abs(A.x - B.x) < EPSILON:
        return point(A.x, C.y, 0)

    if abs(A.y - B.y) < EPSILON:
        return point(C.x, A.y, 0)

    slope = (A.y - B.y)/(A.x - B.x)
    slope2 = -(A.x - B.x)/(A.y - B.y)

    x = (A.y - C.y + slope2*C.x - slope*A.x)/(slope2 - slope)
    y = C.y + slope2*(x - C.x)

    return point(x, y, 0)


def point_on_line(A: point, B: point, C: point) -> bool:
    """
    Determines whether 'C' is in the line AB or not.
    """

    a = A.x - B.x
    b = A.y - B.y
    left_result = a*C.y
    right_result = A.y*a + b*(C.x - A.x)

    if abs(left_result - right_result) < EPSILON:
        return True
    return False


def get_point_end_and_init_paralallel_to_line_on_two_lines(A: point, B: point, C: point, D: point, X: point, Y: point, P: point) -> Tuple[point, point]:
    """
    Given 3 lines: AB, CD and XY; and point 'P', calculate parallel line to XY in point P and get the intersection
    of that line in lines AB and CD. In order, returns the intersection on line AB first then the
    intersection on line CD.
    """

    if point_on_line(X, Y, P):
        return Y, X

    # Slope tends to inifinity:
    if abs(X.x - Y.x) < EPSILON:
        x1, y1 = X.x, 0
        x2, y2 = X.x, 0

        slope1 = (A.y - B.y)/(A.x - B.x)
        y1 = A.y + slope1*(x1 - A.x)

        slope2 = (C.y - D.y)/(C.x - D.x)
        y2 = C.y + slope2*(x2 - C.x)

        return point(x1, y1, 0), point(x2, y2, 0)

    # Slope is 0
    if abs(X.y - Y.y) < EPSILON:
        x1, y1 = 0, X.y
        x2, y2 = 0, X.y

        # Slope tends to infinity
        if abs(A.x - B.x) < EPSILON:
            y1 = A.x
        else:
            slope1 = (A.y - B.y)/(A.x - B.x)
            y1 = A.y + slope1*(x1 - A.x)

        # Slope tends to infinity
        if abs(C.x - D.x) < EPSILON:
            y1 = C.x
        else:
            slope1 = (C.y - D.y)/(C.x - D.x)
            y1 = C.y + slope1*(x1 - C.x)

        return point(x1, y1, 0), point(x2, y2, 0)

    # The slope is normal
    slope = (X.y - Y.y)/(X.x - Y.x)
    arbitrarial_x = P.x + 10
    P2 = point(arbitrarial_x, P.y + slope*(arbitrarial_x - P.x), 0)
    P1 = intersection_point_between_lines(A, B, P, P2)
    P2 = intersection_point_between_lines(C, D, P, P2)

    return P1, P2


def intersection_point_between_lines(A: point, B: point, C: point, D: point) -> point:
    """
    Calculate and return the intersection of line AB and line CD. The function works on the premise
    that AB and CD are not collinear.
    """

    # Line AB represented as a1x + b1y = c1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)

    # Line CD represented as a2x + b2y = c2
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2*(C.x) + b2*(C.y)

    determinant = a1*b2 - a2*b1
    x = (b2*c1 - b1*c2)/determinant
    y = (a1*c2 - a2*c1)/determinant
    return point(x, y, 0)


def point_on_segment(P: point, A: point, B: point) -> bool:
    """
    Determines whether or not the point 'P' is on the segment defined by
    AB.
    """

    a = A.y - B.y
    b = B.x - A.x
    c = A.x*B.y - A.y*B.x

    if (abs(a*P.x + b*P.y + c) < EPSILON):
        x_min = min(A.x, B.x)
        x_max = max(A.x, B.x)
        y_min = min(A.y, B.y)
        y_max = max(A.y, B.y)

        if(x_min < (P.x + EPSILON) and x_max > (P.x - EPSILON) and y_min < (P.y + EPSILON) and y_max > (P.y - EPSILON)):
            return True

    return False


def lines_has_intersection(A: point, B: point, C: point, D: point) -> int:
    """
    Determines whether or not lines AB and CD has intersection. Returns 1 if they
    intersect, 0 otherwise.
    """

    o1 = get_orientation(A, B, C)
    o2 = get_orientation(A, B, D)
    o3 = get_orientation(C, D, A)
    o4 = get_orientation(C, D, B)

    # General case
    if (o1 != o2 and o3 != o4):
        return 1

    if(o1 == COLLINEAR_ORIENTATION and point_on_segment(C, A, B)):
        return 1

    if(o2 == COLLINEAR_ORIENTATION and point_on_segment(D, A, B)):
        return 1

    if(o3 == COLLINEAR_ORIENTATION and point_on_segment(A, C, D)):
        return 1

    if(o4 == COLLINEAR_ORIENTATION and point_on_segment(B, C, D)):
        return 1

    return 0


def does_segments_intersect(A: point, B: point, P: point, Q: point) -> bool:
    """
    Determines wheter segment AB and PQ have an intersection, but doesn't overlap.
    """

    o1 = get_orientation(A, B, P)
    o2 = get_orientation(A, B, Q)
    o3 = get_orientation(P, Q, A)
    o4 = get_orientation(P, Q, B)

    if(o1 + o2 + o3 + o4 == 0):  # Segments AB and PQ overlap.
        return False

    has_intersection = lines_has_intersection(A, B, P, Q)
    if not has_intersection:
        return False

    p_intersection: point = intersection_point_between_lines(A, B, P, Q)
    if point_on_segment(p_intersection, A, B) and point_on_segment(p_intersection, P, Q):
        return True
    return False


def does_segments_overlap(A: point, B: point, P: point, Q: point) -> bool:
    """
    Determines wheter segment AB and PQ overlaps.
    """

    o1 = get_orientation(A, B, P)
    o2 = get_orientation(A, B, Q)
    o3 = get_orientation(P, Q, A)
    o4 = get_orientation(P, Q, B)

    if(o1 + o2 + o3 + o4 == 0):  # Segments AB and PQ overlap.
        if(point_on_segment(A, P, Q) or point_on_segment(B, P, Q) or point_on_segment(P, A, B) or point_on_segment(Q, A, B)):
            return True
    return False


def angle_between_segments(A: point, P: point, B: point):
    """
    Calculates the angle between segment AP and segment PB.
    """

    A_seen_by_P: point = point(A.x - P.x, A.y - P.y, 0)
    B_seen_by_P: point = point(B.x - P.x, B.y - P.y, 0)
    norm_AB = vector_norm(A, P)
    norm_PQ = vector_norm(B, P)
    dot_product = A_seen_by_P.dot_product(B_seen_by_P)

    result = dot_product/(norm_AB*norm_PQ)
    return acos(result)
