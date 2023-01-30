import copy
from math import tan
import math
from typing import Tuple
from drone_vision.lines_operations import get_point_inside_line_by_y_coordinate
from drone_vision.points_operations import vector_norm

from drone_vision.point import point
from drone_vision.quadrilateral import quadrilateral

COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_GRADE_IN_RADIANS = math.pi/180
COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_RADIAN_IN_GRADES = 180/math.pi
MAX_DISTANCE = 400  # measured in meters.
EARTH_RADIUS = 6378137


def get_horizontal_and_vertical_FOV(FOV: float, sensor_diagonal: float, sensor_horizontal: float, sensor_vertical: float) -> Tuple[float, float]:
    """
    Calculates the horizontal and vertical FOV from camera sensor specifications. Returns the horizontal and the vertical field of view respectively.
    """

    focal_lenght: float = (sensor_diagonal/(2*tan(FOV/2))
                           ) * ONE_RADIAN_IN_GRADES
    horizontal_FOV: float = 2 * \
        math.atan(sensor_horizontal/focal_lenght) * ONE_RADIAN_IN_GRADES
    vertical_FOV: float = 2 * \
        math.atan(sensor_vertical/focal_lenght) * ONE_RADIAN_IN_GRADES

    return horizontal_FOV, vertical_FOV


def get_quadrilateral_projection(inclination_theta: float, horizontal_FOV: float, vertical_FOV: float, drone_to_ground_height: float, drone_position: point) -> quadrilateral:
    """
    By using the angles inclination_theta, horizontal_FOV and vertical_FOV and the height
    from the drone to the ground, we project the area that the drone sees in the drone's coordinate
    system, taking z=0 in all the quadrilateral's points. This projection is called Camera Footprint.

    Take note of angles, here they are taken in counter-clockwise, starting from x-axis for rotations
    made in z-axis and starting from x-axis for rotations made in y-axis.
    """

    min_y = -drone_to_ground_height / \
        tan(COMPLETE_CIRCUNFERENCE + ONE_GRADE_IN_RADIANS *
            inclination_theta - ONE_GRADE_IN_RADIANS*vertical_FOV/2)

    max_theta_y = COMPLETE_CIRCUNFERENCE + ONE_GRADE_IN_RADIANS * \
        inclination_theta + ONE_GRADE_IN_RADIANS * vertical_FOV/2

    # ! Angle cant be greater or equal than 360°
    max_theta_y = max_theta_y if max_theta_y < COMPLETE_CIRCUNFERENCE else 359.99
    max_y = -drone_to_ground_height / \
        tan(max_theta_y)

    # ! Maximum distance can't be greater that MAX_DISTANCE meters from the min-y measurement.
    max_y = max_y if max_y < (min_y + MAX_DISTANCE) else (min_y + MAX_DISTANCE)

    min_x = abs(min_y)*tan(ONE_GRADE_IN_RADIANS*horizontal_FOV/2)
    max_x = max_y*tan(ONE_GRADE_IN_RADIANS*horizontal_FOV/2)

    A = point(-max_x, max_y, 0)
    B = point(max_x, max_y, 0)
    C = point(-min_x, min_y, 0)
    D = point(min_x, min_y, 0)

    projected_quadrilateral = quadrilateral(A, B, C, D, drone_position)
    return projected_quadrilateral


def project_detection_on_earth(yaw: float, drone_position: point, normalized_detection: point, drone_vision: quadrilateral) -> point:
    """
    Projects 'normalized_detection' on the earth on (latitude, longitude) coordinates based on
    'drone_position'. To project the point on earth, the 'drone_vision' projected on the ground
    is imperative.
    """

    unrotated_drone_vision: quadrilateral = copy.deepcopy(drone_vision)
    unrotated_drone_vision.rotate(COMPLETE_CIRCUNFERENCE - yaw)

    yf = abs(unrotated_drone_vision.B - unrotated_drone_vision.D)
    Py = drone_vision.D.y + yf*normalized_detection.y

    Ppr = get_point_inside_line_by_y_coordinate(
        drone_vision.D, drone_vision.B, Py)
    Ppl = get_point_inside_line_by_y_coordinate(
        drone_vision.C, drone_vision.A, Py)

    xf = vector_norm(Ppl, origin=Ppr)
    Px = Ppr.x + xf*normalized_detection.x

    P = point(Px, Py, 0)
    P.rotate(yaw)
    P.project_point_on_earth(drone_position)

    return P
