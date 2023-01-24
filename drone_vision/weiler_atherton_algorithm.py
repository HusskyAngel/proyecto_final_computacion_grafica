from typing import List, Tuple

from quadrilateral import quadrilateral
from points_operations import vector_norm
from point import point
from point_entering import PointEntering
from polygon_operations import delete_collinear_segments, point_in_polygon, rotate_polygon, point_in_polygon_perimeter, sort_clockwise_polygon, is_polygon_inside_polygon, delete_repeated_points
from lines_operations import does_segments_intersect, intersection_point_between_lines, does_segments_overlap, point_on_segment


class border_point():
    """
    Contains information about point 'P' like if it's on border of polygon, its index on another polygon in case is border,
    if it belongs to a segment of border points and in case it belongs to some segment of border points it tells wheter
    it's the end of said segment.
    """

    def __init__(self, P: point, is_border: bool, idx: int, is_segment: bool = False, is_end: bool = False):
        """
        idx: index of current point in the polygon list in which it was checked.
        is_border: tells wheter current point lies on the border (perimeter) from some polygon.
        is_segment: tells wheter current point is part of segment of border points.
        is_end: tells wheter current point is the end of segment of border poinst (in case that is segment).
        """
        self.P = P
        self.index = idx
        self.is_border = is_border
        self.is_segment = is_segment
        self.is_end = is_end

    def __str__(self) -> str:
        return f"idx: {self.index}, is_border: {self.is_border}, is_segment: {self.is_segment}, is_end: {self.is_end}"


def check_points_in_perimeter(clipped_polygon: List[point], clipping_polygon: List[point]) -> List[bool]:
    """
    Creates a list of size len(clipping_polygon) that stands True if the i-th point in 'clipping_polygon' is
    on the perimeter of 'clipped_polygon'.
    """

    point_in_perimeter = []

    for p in clipping_polygon:
        point_in_perimeter.append(
            point_in_polygon_perimeter(p, clipped_polygon))

    return point_in_perimeter


def get_segment_intersections(clipped_polygon: List[point], clipping_polygon: List[point], points_on_clipped_perimeter: List[bool]) -> List[List[border_point]]:
    """
    Given 2 polygons 'clipped_polygon' and 'clipping_polygon' determines which segments from 'clipping_polygon'
    intersects with segments of 'clipped_polygon'. Returns a list of indexes starting from 0, i.e intersections[i]
    (where 'i' is the index of some segment of 'clipping_polygon') gives the indexes of some segment from 'clipped_polygon'
    where both segments intersect. Furthermore, the function returns an aditional list that contains points that are at the
    'clipped_polygon' border.
    """

    clipping_polygon_size: int = len(clipping_polygon)
    border_intersections: List[List[border_point]] = []
    for i in range(0, clipping_polygon_size):
        border_intersections.append([])

    for i in range(0, clipping_polygon_size):
        next_index = (i + 1) % clipping_polygon_size
        next_next_index = (i + 2) % clipping_polygon_size
        previous_index = (
            i - 1 + clipping_polygon_size) % clipping_polygon_size
        if(points_on_clipped_perimeter[i] and points_on_clipped_perimeter[next_index]):
            # Exists segment that intersects with clipped_polygon's border.
            continue

        A: point = clipping_polygon[i]
        B: point = clipping_polygon[next_index]

        for j in range(0, len(clipped_polygon)):
            P: point = clipped_polygon[j]
            Q: point = clipped_polygon[(j + 1) % len(clipped_polygon)]

            # Verify overlapping in segments
            if(does_segments_overlap(A, B, P, Q)):
                print(f"Overlap in segments {i} and {j}")
                if point_on_segment(A, P, Q):
                    border_intersections[i].append(
                        border_point(A, True, j, True))
                    border_intersections[i].append(
                        border_point(Q, True, j, True, True))
                elif point_on_segment(B, P, Q):
                    if point_on_segment(P, A, B):
                        border_intersections[i].append(
                            border_point(P, True, j, True))
                        border_intersections[i].append(
                            border_point(B, True, j, True, True))
                    else:
                        border_intersections[i].append(
                            border_point(B, True, j, True, True))
                        border_intersections[i].append(
                            border_point(Q, True, j, True))
                else:
                    border_intersections[i].append(
                        border_point(P, True, j, True))
                    border_intersections[i].append(
                        border_point(Q, True, j, True, True))
                continue

            # Verify intersection in segments
            if(does_segments_intersect(A, B, P, Q)):
                intersection = intersection_point_between_lines(A, B, P, Q)

                # The intersection should not appear twice
                if P.equal(intersection):
                    continue

                # A or B are border points
                if intersection.equal(A) or intersection.equal(B):
                    if intersection.equal(A) and points_on_clipped_perimeter[previous_index]:
                        # intersection is end of border points segments.
                        border_intersections[i].append(
                            border_point(intersection, True, j, True, True))
                    elif intersection.equal(A):
                        # intersection is only one border point.
                        border_intersections[i].append(
                            border_point(intersection, True, j, False))
                    elif points_on_clipped_perimeter[next_next_index]:
                        # intersection point is the begining of border points segment.
                        border_intersections[next_index].append(
                            border_point(intersection, True, j, True))
                    continue

                # Checking the validity of intersection point
                if intersection.equal(Q):
                    # Intersection point equal to point of clipped_polygon
                    current_point = point_in_polygon(A, clipped_polygon)
                    next_point = point_in_polygon(B, clipped_polygon)

                    if current_point ^ next_point:
                        # Intersection is valid
                        border_intersections[i].append(
                            border_point(intersection, False, j))
                else:
                    border_intersections[i].append(
                        border_point(intersection, False, j))

    print("Border points as intersections:", end="[\n")
    for i in range(0, len(border_intersections)):
        print("[", end="")
        for bp in border_intersections[i]:
            print(bp, end=", ")
        print("]")
    print("]")

    return border_intersections


def polish_clipping_polygon_intersections(clipping_polygon: List[point], border_intersections: List[List[border_point]]) -> List[List[border_point]]:
    """
    Sorts every intersection point inside a segment by its vectorial norm.
    """

    for i in range(0, len(clipping_polygon)):
        A = clipping_polygon[i]
        border_intersections[i].sort(key=lambda p: vector_norm(p.P, origin=A))

    print("Sorted border points as intersections:", end="[\n")
    for i in range(0, len(border_intersections)):
        print("[", end="")
        for bp in border_intersections[i]:
            print(bp, end=", ")
        print("]")
    print("]")


def build_clipping_and_clipped_polygon_lists(clipped_polygon: List[point], clipping_polygon: List[point]) -> Tuple[List[PointEntering], List[PointEntering]]:
    """
    Creates and returns 'clipping_polygon' and 'clipped_polygon' list of vertices with their respective intersections.

    Take note that both 'clipped_polygon' and 'clipping_polygon' should be already sorted clockwise.
    """

    clipped_polygon_list: List[PointEntering] = []
    clipping_polygon_list: List[PointEntering] = []
    points_on_clipped_perimeter: List[bool] = check_points_in_perimeter(
        clipped_polygon, clipping_polygon)

    clipping_polygon_border_intersections = get_segment_intersections(
        clipped_polygon, clipping_polygon, points_on_clipped_perimeter)
    polish_clipping_polygon_intersections(
        clipping_polygon, clipping_polygon_border_intersections)

    clipped_polygon_intersections: List[List[PointEntering]] = []
    for i in range(0, len(clipped_polygon)):
        clipped_polygon_intersections.append([])

    # Building preliminar clipping_polygon_list and clipped_polygon_list.
    for i in range(0, len(clipping_polygon)):
        clipping_polygon_list.append(PointEntering(clipping_polygon[i], False))

        for j in range(0, len(clipping_polygon_border_intersections[i])):
            bp: border_point = clipping_polygon_border_intersections[i][j]
            intersection_point = bp.P
            incomplete = True
            single = False
            entering = False
            if not bp.is_border or (bp.is_segment and not bp.is_end):
                incomplete = False

            if bp.is_border and not bp.is_segment:
                single = True

            if not incomplete:
                j = len(clipping_polygon_list) - 1
                while(clipping_polygon_list[j].P.equal(bp.P)):
                    # First point in list its outside clipped_polygon, so it will stop.
                    j -= 1

                last_point = clipping_polygon_list[j]
                entering = not point_in_polygon(last_point.P, clipped_polygon)

            intersection: PointEntering = PointEntering(
                intersection_point, True, entering, incomplete, single)
            clipping_polygon_list.append(intersection)
            clipped_polygon_intersections[bp.index].append(intersection)

    # Completing the clipping_polygon_list
    for i in range(0, len(clipping_polygon_list)):
        pe: PointEntering = clipping_polygon_list[i]
        if not pe.incomplete:
            continue

        clipping_polygon_list[i].incomplete = False
        next_index = (i + 1) % len(clipping_polygon_list)
        while clipping_polygon_list[next_index].P.equal(pe.P):
            next_index = (next_index + 1) % len(clipping_polygon_list)

        previous_index = (i - 1 + len(clipping_polygon_list)
                          ) % len(clipping_polygon_list)
        while clipping_polygon_list[previous_index].P.equal(pe.P):
            previous_index = (
                previous_index - 1 + len(clipping_polygon_list)) % len(clipping_polygon_list)

        if pe.is_single:
            last_point = point_in_polygon(
                clipping_polygon_list[previous_index].P, clipped_polygon)
            next_point = point_in_polygon(
                clipping_polygon_list[next_index].P, clipped_polygon)

            if last_point ^ next_point:
                # point is indeed an intersection.
                clipping_polygon_list[i].entering = not last_point
            else:
                # point should not be counted as intersection
                clipping_polygon_list[i].intersection = False
        else:
            next_point = point_in_polygon(
                clipping_polygon_list[next_index].P, clipped_polygon)
            clipping_polygon_list[i].entering = next_point

    for i in range(0, len(clipped_polygon_intersections)):
        A: point = clipped_polygon[i]
        clipped_polygon_intersections[i].sort(
            key=lambda p: vector_norm(p.P, origin=A))

        clipped_polygon_list.append(PointEntering(A, False))
        for p in clipped_polygon_intersections[i]:
            clipped_polygon_list.append(p)

    for p in clipped_polygon_list:
        p.print()
    print("End of clipped polygon list")
    for p in clipping_polygon_list:
        p.print()
    print("End of clipping polygon list")

    return clipped_polygon_list, clipping_polygon_list


def get_intersection_polygons(clipped_polygon: List[point], clipping_polygon: List[point]) -> List[List[point]]:
    """
    Returns every (if any) intersection polygon in 'clipped_polygon' and 'clipping_polygon'. 'clipped_polygon' should
    always be a convex polygon, i.e. the camera_vision.
    """

    clipping_polygon = sort_clockwise_polygon(clipping_polygon)

    clipping_in_clipped: bool = is_polygon_inside_polygon(
        clipping_polygon, clipped_polygon)

    if(clipping_in_clipped):
        return [clipping_polygon]

    clipping_polygon = delete_collinear_segments(clipping_polygon)

    # We will rotate clipping_polygon till the first point is not inside the polygon.
    # We could actually do this 'cause, as a previous step, we did verify that the polygon its not contained.
    # Thats the reason why it has at least one point outside, and its the one of interest.
    while(point_in_polygon(clipping_polygon[0], clipped_polygon)):
        clipping_polygon = rotate_polygon(clipping_polygon)

    print("Polygon cleaned:")
    for p in clipping_polygon:
        print(p.to_string())
    print("End of cleaned polygon")

    intersection_polygons: List[List[point]] = []

    clipped_polygon_list: List[PointEntering]
    clipping_polygon_list: List[PointEntering]
    clipped_polygon_list, clipping_polygon_list = build_clipping_and_clipped_polygon_lists(
        clipped_polygon, clipping_polygon)

    seen_points: List[bool] = [False] * len(clipping_polygon_list)

    for i in range(0, len(clipping_polygon_list)):
        if(not clipping_polygon_list[i].intersection or not clipping_polygon_list[i].entering or seen_points[i]):
            continue

        P_ini = clipping_polygon_list[i]
        intersection_polygon: List[point] = [P_ini.P]
        j = (i + 1) % len(clipping_polygon_list)
        turn = 1
        seen_points[i] = True
        found_exit = False
        not_exit = True

        while(not_exit):
            if(turn == 1):
                if(seen_points[j]):
                    break
                # print(f"In {j} we have:",
                #       clipping_polygon_list[j].intersection, not clipping_polygon_list[j].entering)
                if(clipping_polygon_list[j].intersection and not clipping_polygon_list[j].entering):
                    found_exit = True
                else:
                    intersection_polygon.append(clipping_polygon_list[j].P)
                    seen_points[j] = True
                    j = (j + 1) % len(clipping_polygon_list)

                # print(
                #     f"Out of exploring clipping_polygon_list with index {j} and point: ", end="")
                # clipping_polygon_list[j].print()

                if(not found_exit):
                    continue

                for k in range(0, len(clipped_polygon_list)):
                    if(clipped_polygon_list[k].equal(clipping_polygon_list[j])):
                        intersection_polygon.append(clipped_polygon_list[k].P)
                        j = (k + 1) % len(clipped_polygon_list)
                        turn = 1 - turn
                        found_exit = False
                        # print(f"Start on clipped_polygon_list in index {j - 1}")
                        break
            else:
                if(P_ini.equal(clipped_polygon_list[j])):
                    break

                intersection_polygon.append(clipped_polygon_list[j].P)
                if(clipped_polygon_list[j].intersection and clipped_polygon_list[j].entering):
                    for k in range(0, len(clipping_polygon_list)):
                        if(clipped_polygon_list[j].equal(clipping_polygon_list[k])):
                            if seen_points[k]:
                                not_exit = False  # Its a loop of points.
                                break
                            seen_points[k] = True
                            turn = 1 - turn
                            j = (k + 1) % len(clipping_polygon_list)
                            break
                else:
                    j = (j + 1) % len(clipped_polygon_list)

        intersection_polygons.append(intersection_polygon)

    if len(intersection_polygons) == 0:
        # It's possible that clipped_polygon it's inside clipoing_polygon
        if is_polygon_inside_polygon(clipped_polygon, clipping_polygon):
            return [clipped_polygon]
    return delete_repeated_points(intersection_polygons)


def calculate_polygon_intersection(camera_projection: quadrilateral, polygon: List[point]) -> Tuple[bool, List[List[point]]]:
    """
    Calculate and return the intersection (if any) between 'camera_projection' and 'polygon'.

    Returns:
    has_intersection: boolean, polygons_intersections: List[List[point]]
    """

    camera_projection_formatted = camera_projection.to_weilmar_atherton_representation()

    polygon_intersections: List[List[point]] = get_intersection_polygons(
        camera_projection_formatted, polygon)

    if len(polygon_intersections) == 0:
        return False, None

    return True, polygon_intersections
