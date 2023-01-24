import math
from typing import List
from point import point

COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_GRADE_IN_RADIANS = math.pi/180
COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_RADIAN_IN_GRADES = 180/math.pi
EARTH_RADIUS = 6378137


class quadrilateral(object):
    """
    This class contains 4 points, being (x, y, z) or (θ, φ, R) coordinates, where
    theta is latitude and phi is longitude. This beforementioned points represents
    the quadrilateral, and this coordinates are relative to one point on earth
    given by (theta, phi, radius) coordinates, the drone position on earth.
    """

    def __init__(self, A: point, B: point, C: point, D: point, drone_position: point):
        """
        Initialize projected quadrilateral on the form:\n
        ..A----------B..\n
        .....C----D.....
        """
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.drone_position = drone_position

    def rotate(self, rotation_angle: float):
        """
        Rotates the quadrilateral in 'rotation_angle' seen by the real world coordinate system instead
        of the camera one.
        """

        # This is because we want to rotate the vectors counter-clockwise so the y-axis
        # points directly to the north, but the rotation_angle is measured clockwise, so
        # we do the equivalence of this angle by doing the rotation in the opposite sense.
        BETA = COMPLETE_CIRCUNFERENCE - rotation_angle*ONE_GRADE_IN_RADIANS
        self.A.rotate(BETA)
        self.B.rotate(BETA)
        self.C.rotate(BETA)
        self.D.rotate(BETA)

    def translate(self, origin_point: point):
        """
        Translate the quadrilateral to be seen from 'origin_point'. This is vectorial sum.
        """
        self.A.translate(origin_point)
        self.B.translate(origin_point)
        self.C.translate(origin_point)
        self.D.translate(origin_point)

    def project_on_earth(self):
        """
        Transform (x, y, z) coordinates to (θ, φ, R) coordinates.
        """
        self.A.project_point_on_earth(self.drone_position)
        self.B.project_point_on_earth(self.drone_position)
        self.C.project_point_on_earth(self.drone_position)
        self.D.project_point_on_earth(self.drone_position)

    def project_on_plane(self):
        """
        Transform (θ, φ, R) 'quadrilateral' coordinates to (x, y, z) coordinates.
        """
        self.A.project_point_to_plane(self.drone_position)
        self.B.project_point_to_plane(self.drone_position)
        self.C.project_point_to_plane(self.drone_position)
        self.D.project_point_to_plane(self.drone_position)

    def to_weilmar_atherton_representation(self) -> List[point]:
        """
        Represent the quadrilateral as a list of points.
        """

        return [self.A, self.B, self.D, self.C]
