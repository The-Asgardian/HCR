import os
import sys

import cv2
from controller import Robot

VISION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "vision"))
sys.path.append(VISION_DIR)

from camera import open_camera
from hands import create_detector, find_hands, draw_hands
from gestures import classify

SPEED = 3.0
TURN = 2.0

robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

capture = open_camera()
detector = create_detector()


def command_to_speeds(command):
    if command == "FORWARD":
        return SPEED, SPEED
    if command == "BACKWARD":
        return -SPEED, -SPEED
    if command == "LEFT":
        return -TURN, TURN
    if command == "RIGHT":
        return TURN, -TURN
    return 0.0, 0.0


while robot.step(timestep) != -1:
    ok, frame = capture.read()
    if not ok:
        continue
    frame = cv2.flip(frame, 1)
    result = find_hands(detector, frame)
    draw_hands(frame, result)
    command = classify(result)
    cv2.putText(frame, command, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow("Gestures", frame)
    cv2.waitKey(1)
    left_speed, right_speed = command_to_speeds(command)
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
