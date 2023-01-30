import matplotlib.pyplot as plt
from drone_vision.point import point
from drone_vision.camera_projections import get_quadrilateral_projection, get_horizontal_and_vertical_FOV
from drone_vision.polygon_operations import format_simple_polygon
from drone_vision.weiler_atherton_algorithm import calculate_polygon_intersection

x, y, z = 0, 0, 45
inclination_theta = -30  # should be in range [-90, 0]
FOV = 84
yaw = 210
sensor_diagonal = 8  # This is given in mm.
sensor_horizontal = 6.4  # mm
sensor_vertical = 4.8  # mm
HFOV, VFOV = get_horizontal_and_vertical_FOV(
    FOV, sensor_diagonal, sensor_horizontal, sensor_vertical)
drone_position = point(x, y, z)

camera_footprint = get_quadrilateral_projection(
    inclination_theta, HFOV, VFOV, z, drone_position)
camera_footprint.translate(point(x, y, 0))
# camera_footprint.rotate(yaw)

camera_footprint_coords = []
camera_footprint_points = camera_footprint.to_weilmar_atherton_representation()
for p in camera_footprint_points:
    camera_footprint_coords.append([p.x, p.y])

camera_footprint_coords.append(camera_footprint_coords[0])

# Read polygon
coord = [[20, 75], [10, 60], [0, 72], [12, 74], [0, 75], [10, 85]]

polygon = format_simple_polygon(coord)

has_intersection, intersection_polygons = calculate_polygon_intersection(
    camera_footprint, polygon)


coord.append(coord[0])  # repeat the first point to create a 'closed loop'

xs, ys = zip(*coord)  # create lists of x and y values
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
