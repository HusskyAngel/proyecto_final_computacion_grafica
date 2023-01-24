import math

from point import point
from quadrilateral import quadrilateral
from weiler_atherton_algorithm import calculate_polygon_intersection

COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_GRADE_IN_RADIANS = math.pi/180
ONE_RADIAN_IN_GRADES = 180/math.pi
EARTH_RADIUS = 6378137
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
EPSILON = 0.00001

drone_position = point(3.5572512, -76.4239383, EARTH_RADIUS)

A = point(3, 9, 0)
B = point(9, 3, 0)
C = point(1, 3, 0)
D = point(3, 1, 0)

camera = quadrilateral(A, B, C, D, drone_position)

S1 = point(0, 8, 0)
S2 = point(3.5, 10, 0)
S3 = point(3, 5, 0)
S4 = point(6, 7.5, 0)
S5 = point(6, 3.5, 0)
S6 = point(10, 12, 0)
S7 = point(2, 11, 0)
S8 = point(10, 1, 0)
S9 = point(0, 5, 0)
S10 = point(0, 0, 0)
S11 = point(3, 3, 0)
S12 = point(3, 9, 0)
S13 = point(5, 7, 0)
S14 = point(7, 5, 0)
S15 = point(11, 4, 0)
S16 = point(3, 10, 0)
S17 = point(3, -1, 0)
S18 = point(0, 1, 0)
S19 = point(4, 12, 0)
S20 = point(11, 1, 0)
S21 = point(-1, 5, 0)
S22 = point(2, 2, 0)
S23 = point(6, 2, 0)
S24 = point(8, 8, 0)

ALlPoints = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12,
             S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23, S24]

for i in range(0, len(ALlPoints)):
    p = ALlPoints[i]
    print(f"S{i + 1} = ({p.x:.2f}, {p.y:.2f})")

# Every polygon segment is given in clockwise order
Polygon = [S1, S7, S6, S5, S4, S3, S2]
Polygon_ccw = [S2, S3, S4, S5, S6, S7, S1]
Polygon2 = [S1, S7, S6, S3, S2]
Polygon3 = [S8, S1, S2, S6]
Polygon4 = [S9, S2, S3, S6, S8]
Polygon5 = [S3, S5, S11]
Polygon6 = [S10, S1, S2, S6, S8]
Polygon7 = [S10, S6, S8]
Polygon8 = [S11, S12, S6, S8]
Polygon9 = [S12, S13, S6, S14, S15, S8, S3]
Polygon10 = [S12, S13, S14, B, S5, S3]
Polygon11 = [S14, S13, S12, S2, S6, B]
Polygon12 = [S2, S15, B, S14, S5, S4, S13, S12]
Polygon13 = [S17, S16, S15, S5, S8]
Polygon14 = [S6, S8, D]
Polygon15 = [S15, S8, D, A]
Polygon16 = [S18, S9, S13, B, D]
Polygon17 = [S1, S6, S13, S14, S15, S8, S11, S3]
Polygon18 = [S10, S19, S15, S5, S8]
Polygon19 = [S20, S11, S5, S14]
Polygon20 = [S9, S7, S12]
Polygon21 = [S24, S23, S10, S21, S22]
Polygon22 = [S18, S8, S17]
Polygon23 = [S17, S20, S23]
Polygon24 = [S20, S6, S12, S3, S13, S14, S5, B]

# gives [[(6.80 5.20), (6.00 3.50), (6.00 6.00)], [(5.18 6.82), (3.00 5.00), (3.36 8.64)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon)

# gives [[(5.00 7.00), (3.00 5.00), (3.36 8.64)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon2)

# gives [[(7.74 2.58), (2.16 6.49), (3.00 9.00), (9.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon3)

# gives [[(3.36 8.64), (3.00 5.00), (5.00 7.00), (9.00 3.00), (6.82 2.27), (1.47 4.41), (3.00 9.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon4)

# gives [[(3.00 5.00), (6.00 3.50), (3.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon5)

# gives [[(3.00 9.00), (9.00 3.00), (3.00 1.00), (1.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon6)

# gives [[(1.82 2.18), (5.45 6.55), (9.00 3.00), (3.00 1.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon7)

# gives [[(6.23 2.08), (3.00 3.00), (3.00 9.00), (9.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon8)

# gives [[(7.00 5.00), (9.00 3.00), (7.42 2.47), (3.00 5.00), (3.00 9.00), (5.00 7.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon9)

# gives [[(3.00 9.00), (5.00 7.00), (7.00 5.00), (9.00 3.00), (6.00 3.50), (3.00 5.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon10)

# gives [[(9.00 3.00), (3.00 9.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon11)

# gives [[(9.00 3.00), (7.00 5.00), (6.00 3.50), (6.00 6.00), (7.00 5.00)], [(5.00 7.00), (3.00 9.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon12)

# gives [[(3.00 1.00), (3.00 9.00), (8.27 3.73), (6.00 3.50), (7.57 2.52)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon13)

# gives [[(3.00 1.00), (6.11 5.89), (9.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon14)

# gives [[(3.00 1.00), (3.00 9.00), (9.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon15)

# gives [[(1.92 5.77), (5.00 7.00), (9.00 3.00), (3.00 1.00), (1.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon16)

# gives [[(5.00 7.00), (7.00 5.00), (9.00 3.00), (6.23 2.08), (3.00 3.00), (3.00 5.00), (2.00 6.00), (3.00 9.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon17)

# gives [[(1.00 3.00), (3.00 9.00), (8.27 3.73), (6.00 3.50), (7.57 2.52), (3.00 1.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon18)

# gives [[(6.43 2.14), (3.00 3.00), (6.00 3.50), (7.00 5.00), (9.00 3.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon19)

# gives [[]]
# has_intersection, intersetion_polygons = calculate_polygon_intersection(
#     camera, Polygon20)

# gives [[(7.00 5.00), (6.00 2.00), (3.00 1.00), (2.00 2.00), (6.00 6.00)]]
# intersetion_polygons = calculate_polygon_intersection(camera, Polygon21)

# gives [[]]
# has_intersection, intersetion_polygons = calculate_polygon_intersection(camera, Polygon22)

# gives [[]]
# has_intersection, intersetion_polygons = calculate_polygon_intersection(
#     camera, Polygon23)

# gives [[(9.00 3.00), (6.00 3.50), (7.00 5.00)], [(5.00 7.00), (3.00 5.00), (3.00 9.00)]]
has_intersection, intersetion_polygons = calculate_polygon_intersection(
    camera, Polygon24)

print(f"Polygon intersection: {has_intersection}")
if has_intersection:
    for polygon in intersetion_polygons:
        for p in polygon:
            print(p.to_string())
        print()
