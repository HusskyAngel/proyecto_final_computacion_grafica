import copy
from typing import List, Tuple
from math import acos, floor, sqrt, pi

from drone_vision.point import point
from drone_vision.quadrilateral import quadrilateral
from drone_vision.lines_operations import point_on_line, get_point_end_and_init_paralallel_to_line_on_two_lines, project_point_on_line
from drone_vision.points_operations import vector_norm

EPSILON = 0.00001
ONE_RADIAN_IN_GRADES = 180/pi
COLLINEAR_ORIENTATION = 0
CLOCKWISE_ORIENTATION = 1
COUNTERCLOCKWISE_ORIENTATION = 2


def project_point_on_camera_frame(horizontal_FOV: float, vertical_FOV: float, drone_to_ground_height: float, frame_width: int, frame_height: int, camera_vision: quadrilateral, objetive_point: point) -> List[float]:
    """
    Project 'objetive_point' in the camera frame by calculating the angles formed in drone_position to ground
    to 'objetive_point' and the leftmost line of projected 'camera_vision' on the ground to 'objetive_point'.

    Returns:
    (x, y) coordinates on camera frame.
    """

    camera_frame_theta_x: float = 0
    camera_frame_theta_y: float = 0
    projection_point_y: point = copy.deepcopy(objetive_point)
    DC: point = point((camera_vision.D.x + camera_vision.C.x)/2,
                      (camera_vision.D.y + camera_vision.C.y)/2, 0)
    BA: point = point((camera_vision.B.x + camera_vision.A.x)/2,
                      (camera_vision.B.y + camera_vision.A.y)/2, 0)

    P_begin, P_end = get_point_end_and_init_paralallel_to_line_on_two_lines(
        camera_vision.A, camera_vision.C, camera_vision.B, camera_vision.D, camera_vision.D, camera_vision.C, objetive_point)

    # print("Point begin: ", f'({P_begin.x}, {P_begin.y})')
    # print("Point end: ", f'({P_end.x}, {P_end.y})')

    ONE_GRADE_IN_HEIGHT_PIXELS = frame_height/vertical_FOV
    ONE_GRADE_IN_WIDTH_PIXELS = frame_width/horizontal_FOV

    # objetive point is not the intersection in line formed by DC and BA.
    if not point_on_line(DC, BA, objetive_point):
        projection_point_y = project_point_on_line(
            DC, BA, objetive_point)

    # Grades in x are different to 0
    if not P_begin.equal(objetive_point):
        # Grades in x are equal to horizontal_FOV
        if P_end.equal(objetive_point):
            camera_frame_theta_x = horizontal_FOV
        else:
            begin_to_end = vector_norm(P_begin, origin=P_end)
            begin_to_p = vector_norm(P_begin, origin=objetive_point)
            camera_frame_theta_x = (
                horizontal_FOV*begin_to_p)/(begin_to_end)

    # print("X grades: ", camera_frame_theta_x)
    # Grades in y are different to 0
    if not projection_point_y.equal(point(0, 0, 0)) or not projection_point_y.equal(DC):

        if not point_on_line(camera_vision.C, camera_vision.D, projection_point_y):
            po = sqrt(vector_norm(projection_point_y)
                      ** 2 + drone_to_ground_height**2)
            odc = sqrt(vector_norm(DC) **
                       2 + drone_to_ground_height**2)
            pdc = vector_norm(projection_point_y, origin=DC)

            camera_frame_theta_y = acos(
                (po**2 + odc**2 - pdc**2)/(2*po*odc))*ONE_RADIAN_IN_GRADES

    projected_point_x: int = floor(
        camera_frame_theta_x*ONE_GRADE_IN_WIDTH_PIXELS + EPSILON)
    projected_point_y: int = floor(
        camera_frame_theta_y*ONE_GRADE_IN_HEIGHT_PIXELS + EPSILON)

    return [projected_point_x, frame_height - projected_point_y]
