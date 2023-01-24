from math import acos, cos, sin, sqrt
import math
import copy
from typing import List

COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_GRADE_IN_RADIANS = math.pi/180
COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_RADIAN_IN_GRADES = 180/math.pi
EARTH_RADIUS = 6378137
EPSILON = 0.0000001


class point(object):
    """
    Point instance in 3d coordinate system, being one of the following:
    - (x, y, z)
    - (θ, φ, R)
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Point costructor:
        - (x, y, z)
        - (θ = x, φ = y, R = z)
        """
        self.x = x
        self.y = y
        self.z = z

        # equally:
        self.theta = x
        self.phi = y
        self.R = z

    def rotate(self, beta: float):
        """
        Rotates the actual point by 'beta' degrees in counter-clocwise.
        """
        x = self.x*cos(beta) - self.y*sin(beta)
        y = self.x*sin(beta) + self.y*cos(beta)
        self.x = self.theta = x
        self.y = self.phi = y

    def translate(self, translation_point: 'point'):
        """
        Translate the origin point by 'translation_point'.
        """
        self.x += translation_point.x
        self.y += translation_point.y
        self.theta = self.x
        self.phi = self.y
        # Z its omitted.

    def calculate_delta_latitude(objetive_point: 'point') -> float:
        """
        Calculate the variance on latitude from the drone position on projected plane,
        i.e. drone on (x=0, y=0, z=0), to objetive point measured on this projected plane.
        """

        latitude_height = objetive_point.y
        theta = acos(1 - (latitude_height ** 2)/(2*(EARTH_RADIUS ** 2)))

        # Objetive point is practically in the same position as drone
        if(abs(theta) < EPSILON):
            return 0.0

        # We maintain the polarity of angle.
        theta *= latitude_height/abs(latitude_height)
        return theta

    def calculate_delta_longitude(objetive_point: 'point') -> float:
        """
        Calculate the variance on longitude from the drone position on projected plane,
        i.e. drone on (x=0, y=0, z=0), to objetive point measured on this projected plane.
        """

        longitude_height = objetive_point.x
        phi = acos(1 - (longitude_height ** 2)/(2*(EARTH_RADIUS ** 2)))

        # Objetive point is practically in the same position as drone
        if(abs(phi) < EPSILON):
            return 0.0

        # We maintain the polarity of angle.
        phi *= longitude_height/abs(longitude_height)
        return phi

    def project_point_on_earth(self, drone_position: 'point'):
        """
        Project 'objetive_point' on earth, getting its latitude and longitude
        relative to drone_position.
        """

        delta_theta = self.calculate_delta_latitude()*ONE_RADIAN_IN_GRADES
        delta_phi = self.calculate_delta_longitude()*ONE_RADIAN_IN_GRADES
        # We need a copy of drone position.
        new_position: point = copy.deepcopy(drone_position)
        new_position.translate(point(delta_theta, delta_phi, 0))
        self.x = self.theta = new_position.x
        self.y = self.phi = new_position.y

    def project_point_to_plane(self, drone_position: 'point'):
        """
        Project point to planar surface, calculating (x, y, z) from
        drone_position and point with deltas in latitude and longitude.
        """
        delta_theta = self.theta - drone_position.theta
        delta_phi = self.phi - drone_position.phi
        x = 0.0
        y = 0.0

        if(abs(delta_phi) > 0.000000001):
            x = EARTH_RADIUS*sqrt(2*(1 - cos(delta_phi*ONE_GRADE_IN_RADIANS)))
            x *= delta_phi/abs(delta_phi)

        if(abs(delta_theta) > 0.000000001):
            y = EARTH_RADIUS * \
                sqrt(2*(1 - cos(delta_theta*ONE_GRADE_IN_RADIANS)))
            y *= delta_theta/abs(delta_theta)

        self.x = self.theta = x
        self.y = self.phi = y

    def equal(self, B: 'point') -> bool:
        """
        Compares whether points A and B are equal or not.
        """
        if abs(self.x - B.x) > EPSILON or abs(self.y - B.y) > EPSILON:
            return False
        return True

    def dot_product(self, B: 'point') -> float:
        """
        Return dot product between self and B.
        """

        return self.x*B.x + self.y*B.y

    def to_string(self):
        return f"{self.x:.2f} {self.y:.2f}"
