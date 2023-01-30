from typing import List
import matplotlib.pyplot as plt
from drone_vision.point import point
from drone_vision.camera_projections import get_quadrilateral_projection, get_horizontal_and_vertical_FOV
from drone_vision.polygon_operations import format_simple_polygon
from drone_vision.weiler_atherton_algorithm import calculate_polygon_intersection


def draw_intersection(x: float, y: float, z: float, inclination_theta: float, yaw: float, coord_polygon: List[List[float]]) -> None:
    """
    Given the position of the drone as x,y,z; its inclination angle for the camera, the yaw and a zone of interest ('coord_polygon'),
    calculates the intersection between the camera footprint of the drone and the simple polygon given.
    """
    FOV = 84
    sensor_diagonal = 8  # This is given in mm.
    sensor_horizontal = 6.4  # mm
    sensor_vertical = 4.8  # mm
    HFOV, VFOV = get_horizontal_and_vertical_FOV(
        FOV, sensor_diagonal, sensor_horizontal, sensor_vertical)
    drone_position = point(x, y, z)

    camera_footprint = get_quadrilateral_projection(
        inclination_theta, HFOV, VFOV, z, drone_position)
    camera_footprint.translate(point(x, y, 0))
    camera_footprint.rotate(yaw)

    camera_footprint_coords = []
    camera_footprint_points = camera_footprint.to_weilmar_atherton_representation()
    for p in camera_footprint_points:
        camera_footprint_coords.append([p.x, p.y])

    camera_footprint_coords.append(camera_footprint_coords[0])

    polygon = format_simple_polygon(coord_polygon)

    has_intersection, intersection_polygons = calculate_polygon_intersection(
        camera_footprint, polygon)

    # repeat the first point to create a 'closed loop'
    coord_polygon.append(coord_polygon[0])

    xs, ys = zip(*coord_polygon)  # create lists of x and y values
    xcf, ycf = zip(*camera_footprint_coords)

    plt.figure()
    plt.plot(xs, ys)
    plt.plot(xcf, ycf)

    if has_intersection:
        for polygon in intersection_polygons:
            points = []
            for p in polygon:
                points.append([p.x, p.y])

            xip, yip = zip(*points)
            plt.fill(xip, yip, facecolor="lightgreen",
                     edgecolor='green')

    plt.show()
