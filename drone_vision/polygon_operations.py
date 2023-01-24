import math
from typing import List, Tuple

from geometric_operations import project_point_on_camera_frame
from point import point
from quadrilateral import quadrilateral
from points_operations import get_orientation
from lines_operations import point_on_segment, angle_between_segments

EPSILON = 0.00001
CLOCKWISE_ORIENTATION = 1
COUNTERCLOCKWISE_ORIENTATION = 2


def project_polygon_on_camera_frame(horizontal_FOV: float, vertical_FOV: float, drone_to_ground_height: float, frame_width: int, frame_height: int, camera_vision: quadrilateral, polygon: List[point]) -> List[List[float]]:
    """
    Project 'polygon' in the camera frame by calculating the angles formed in drone_position to ground
    and the leftmost line of projected 'camera_vision' on the ground so we can indicate what the drone
    is seeing in the ground on its frame.
    """

    polygon_projected_on_frame = []

    for p in polygon:
        polygon_projected_on_frame.append(project_point_on_camera_frame(
            horizontal_FOV, vertical_FOV, drone_to_ground_height, frame_width, frame_height, camera_vision, p))

    return polygon_projected_on_frame


def format_polygon(polygon: List[List[float]], drone_position: point) -> List[point]:
    """
    Transform all the points of 'polygon' to custom class point (θ, φ, R)
    and project the point on plane relative to 'drone_position'.
    """

    formatted_polygon: List[point] = []

    for p in polygon:
        formatted_point = point(p[0], p[1], 0)
        formatted_point.project_point_to_plane(drone_position)
        formatted_polygon.append(formatted_point)

    return formatted_polygon


def delete_collinear_segments(polygon: List[point]) -> bool:
    """
    Given 2 contiguous segments, if they are collinear the 2 segments will be joined in only one.
    Namely, given 2 segments AB and BC, if they are collinear those 2 segments now will be just one: AC.

    Returns the polygon without contiguous collinear segments.
    """

    pos: int = 0

    # We look the first point that its not included in 2 segments that are collinear.
    for i in range(0, len(polygon)):
        A = polygon[(i - 1 + len(polygon)) % len(polygon)]
        B = polygon[i]
        C = polygon[(i + 1) % len(polygon)]

        if(get_orientation(A, B, C) == 0):
            continue

        pos = i
        break

    neo_polygon: List[point] = [polygon[pos]]

    for i in range(pos + 1, len(polygon)):
        A = neo_polygon[len(neo_polygon) - 1]
        B = polygon[i]
        C = polygon[(i + 1) % len(polygon)]

        if(get_orientation(A, B, C) == 0):
            continue

        neo_polygon.append(polygon[i])
    return neo_polygon


def point_in_polygon(P: point, polygon: List[point]) -> bool:
    """
    Determines whether or not some point 'p' is inside the given 'polygon'.
    """

    angle_sum = 0

    for i in range(0, len(polygon)):
        j = (i + 1) % len(polygon)
        if point_on_segment(P, polygon[i], polygon[j]):
            return True

        orientation = get_orientation(polygon[i], P, polygon[j])

        if orientation == COUNTERCLOCKWISE_ORIENTATION:
            angle_sum += angle_between_segments(polygon[i], P, polygon[j])
        else:
            angle_sum -= angle_between_segments(polygon[i], P, polygon[j])

    if abs(angle_sum) > math.pi:
        return True

    return False


def rotate_polygon(polygon: List[point]) -> List[point]:
    """
    Rotates the polygon one position to right.
    """

    return polygon[1:] + polygon[:1]


def point_in_polygon_perimeter(P: point, polygon: List[point]) -> bool:
    """
    Determines wheter point 'P' is on the perimeter of 'polygon'.
    """

    for i in range(0, len(polygon)):
        A = polygon[i]
        B = polygon[(i + 1) % len(polygon)]
        if point_on_segment(P, A, B):
            return True

    return False


def polygon_area(polygon: List[point]) -> float:
    """
    Calculates the area of 'polygon'.
    """
    area = 0.0

    for i in range(0, len(polygon)):
        A = polygon[i]
        B = polygon[(i + 1) % len(polygon)]

        area += (A.x*B.y - B.x*A.y)/2

    print(f"Polygon area = {area}")
    return area


def sort_clockwise_polygon(polygon: List[point]) -> List[point]:
    """
    Sorts 'polygon' in clockwise order.
    """

    area = polygon_area(polygon)

    if(area < 0):
        return polygon

    sorted_polygon: List[point] = []

    for i in range(len(polygon) - 1, -1, -1):
        sorted_polygon.append(polygon[i])

    return sorted_polygon


def is_polygon_inside_polygon(A: List[point], B: List[point]) -> bool:
    """
    Determines wheter or not polygon 'A' is inside polygon 'B'.
    """

    count = 0
    for p in A:
        if(not point_in_polygon(p, B)):
            break
        count += 1

    return (count == len(A))


def delete_repeated_points(polygons: List[List[point]]) -> List[List[point]]:
    """
    Deletes repeated points in list of polygons.
    """

    neo_polygons: List[List[point]] = []
    for polygon in polygons:
        neo_polygon: List[point] = []
        for i in range(0, len(polygon)):
            A = polygon[i]
            B = polygon[(i + 1) % len(polygon)]

            if(A.equal(B)):
                continue
            neo_polygon.append(A)

        neo_polygons.append(neo_polygon)

    return neo_polygons
