import cv2
import math
from typing import List, Tuple
import numpy as np

from point import point
from inference_interest_area import get_inference_polygons, getInferenceInterestArea

COMPLETE_CIRCUNFERENCE = 2*math.pi
ONE_GRADE_IN_RADIANS = math.pi/180
ONE_RADIAN_IN_GRADES = 180/math.pi
EARTH_RADIUS = 6378137
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
EPSILON = 0.00001

drone_position = point(3.5572512, -76.4239383, EARTH_RADIUS)
inclination_theta = -45
horizontal_FOV = 120
vertical_FOV = 60
drone_to_ground_height = 40
yaw = 234
restriction_polygons: List[List[Tuple[float, float]]] = [[[3.5567122111, -76.4233993111],
                                                          [3.5577003580, -
                                                              76.4234891420],
                                                          [3.5568020420, -
                                                              76.4243874580],
                                                          [3.5565325477, -
                                                              76.4242077951]
                                                          ]]

frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3))


# Testing the functions
drone_position = point(3.5572512, -76.4239383, EARTH_RADIUS)
polygons_to_make_inferences_on = get_inference_polygons(drone_position, inclination_theta, horizontal_FOV,
                                                        vertical_FOV, drone_to_ground_height, yaw, frame, restriction_polygons)

image = getInferenceInterestArea(frame, polygons_to_make_inferences_on)

while True:
    cv2.imshow("Inference on Black", image)
    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break
