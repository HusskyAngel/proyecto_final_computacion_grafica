import copy
from typing import List
import cv2
import numpy as np

from camera_projections import get_quadrilateral_projection
from geometric_operations import project_point_on_line
from point import point
from polygon_operations import format_polygon, project_polygon_on_camera_frame
from weiler_atherton_algorithm import calculate_polygon_intersection


def drawInferenceMask(polygons: np.ndarray, height: int, width: int):
    """
    Draw a mask composed of white and black colours with 255 and 0 values respectively, where the 255
    (white colour) means that the area (i.e. an area of white pixels) is the interest zone to do
    inference on. This function draws the set of polygons specified on 'polygons', creating all the
    interest zones in a mask of size 'height' * 'width'.
    """
    mask = np.zeros((height, width))

    for polygon in polygons:
        polygon = np.array(polygon)
        cv2.fillPoly(mask, pts=[polygon], color=(255, 255, 255))

    return mask


def getInferenceInterestArea(frame: np.ndarray, polygons: List[List[List[float]]]):
    """
    Transform all the area that is not of interest (area outside the polygons specified on 'polygons')
    in white pixels, where the yolo engine will not recognize anything (hopefully) in the 'frame'. This
    way, we force the yolo engine to make inference on the area where we want it to do it.
    """
    height, width = len(frame), len(frame[0])
    mask = drawInferenceMask(polygons, height, width)
    WHITE = 255
    AREA_OF_INTEREST = (WHITE, WHITE, WHITE)  # This is color white

    for i in range(0, height):
        for j in range(0, width):
            if mask[i][j] != WHITE:
                # We paint every pixel that its outside the area o interest of white
                frame[i][j] = AREA_OF_INTEREST

    return frame


def get_inference_polygons(drone_position: point, inclination_theta: float, horizontal_FOV: float, vertical_FOV: float, drone_to_ground_height: float, yaw: float, frame: np.ndarray, polygons: List[List[List[float]]]) -> List[List[List[float]]]:
    """
    Calculates the coordinates of polygons (if any) that intersects the frame vision on the ground and the
    restriction zones especified on 'polygons'. Note: the coordinates would be represented on pixels on the
    actual frame, not on the ground.
    """

    frame_height = len(frame)
    frame_width = len(frame[0])

    projected_camera_vision = get_quadrilateral_projection(
        inclination_theta, horizontal_FOV, vertical_FOV, drone_to_ground_height, drone_position)
    projected_camera_vision.rotate(yaw)
    print(f"A: {projected_camera_vision.A.to_string()}")
    print(f"B: {projected_camera_vision.B.to_string()}")
    print(f"C: {projected_camera_vision.C.to_string()}")
    print(f"D: {projected_camera_vision.D.to_string()}")

    projected_camera_vision_on_earth = copy.deepcopy(projected_camera_vision)
    projected_camera_vision_on_earth.project_on_earth()

    camera_projected_polygons: List[List[List[float]]] = []

    for polygon in polygons:
        formatted_polygon = format_polygon(polygon, drone_position)

        # for p in formatted_polygon:
        #     print(f'{p.x} {p.y}')

        has_intersection, polygons_intersections = calculate_polygon_intersection(
            projected_camera_vision, formatted_polygon)

        if has_intersection:
            # print("Polygon intersection")
            # for p in polygon_intersection:
            #     print(f'({p.x}, {p.y})')
            # print("End polygon intersection")

            for intersection_polygon in polygons_intersections:
                camera_projected_polygon = project_polygon_on_camera_frame(
                    horizontal_FOV, vertical_FOV, drone_to_ground_height, frame_width, frame_height, projected_camera_vision, intersection_polygon)
                camera_projected_polygons.append(camera_projected_polygon)

    return camera_projected_polygons
