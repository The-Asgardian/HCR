import math
import os
import sys

import cv2
from controller import Robot

VISION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "vision"))
sys.path.append(VISION_DIR)

from camera import open_camera
from hands import create_detector, find_hands, draw_hands
from gestures import classify, Stabilizer

WHEEL_RADIUS = 0.033
WHEEL_SEPARATION = 0.16
DRIVE_SPEED = 3.0
TURN_SPEED = 3.0
HEADING_TOLERANCE = 0.1

TARGET_YAW = {
    "NORTH": math.pi / 2,
    "EAST": 0.0,
    "SOUTH": -math.pi / 2,
    "WEST": math.pi,
}

robot = Robot()
timestep = int(robot.getBasicTimeStep())
dt = timestep / 1000.0

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

capture = open_camera()
detector = create_detector()
stabilizer = Stabilizer()

yaw = math.pi / 2


def angle_diff(a, b):
    d = a - b
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    return d


def speeds_for(command, heading):
    if command not in TARGET_YAW:
        return 0.0, 0.0
    error = angle_diff(TARGET_YAW[command], heading)
    if abs(error) > HEADING_TOLERANCE:
        if error > 0:
            return -TURN_SPEED, TURN_SPEED
        return TURN_SPEED, -TURN_SPEED
    return DRIVE_SPEED, DRIVE_SPEED


while robot.step(timestep) != -1:
    ok, frame = capture.read()
    if not ok:
        continue
    frame = cv2.flip(frame, 1)
    result = find_hands(detector, frame)
    draw_hands(frame, result)
    command = stabilizer.update(classify(result))
    cv2.putText(frame, command, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow("Gestures", frame)
    cv2.waitKey(1)
    left_speed, right_speed = speeds_for(command, yaw)
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    yaw += WHEEL_RADIUS * (right_speed - left_speed) / WHEEL_SEPARATION * dt
