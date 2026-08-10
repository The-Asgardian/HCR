import os
import sys

import cv2
from controller import Robot

VISION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "vision"))
sys.path.append(VISION_DIR)

from camera import open_camera
from hands import create_detector, find_hands, draw_hands
from gestures import classify, Stabilizer

WHEEL_RADIUS = 0.05
SPEED_PER_LEVEL = 0.14
DETECT_EVERY = 4
GOAL = (2.0, 2.0)
GOAL_RADIUS = 0.5

DIRECTION = {
    "NORTH": (0.0, 1.0),
    "SOUTH": (0.0, -1.0),
    "EAST": (1.0, 0.0),
    "WEST": (-1.0, 0.0),
}

robot = Robot()
timestep = int(robot.getBasicTimeStep())

wheels = [robot.getDevice("wheel1"), robot.getDevice("wheel2"), robot.getDevice("wheel3"), robot.getDevice("wheel4")]
for wheel in wheels:
    wheel.setPosition(float("inf"))
    wheel.setVelocity(0.0)

gps = robot.getDevice("gps")
if gps:
    gps.enable(timestep)
else:
    print("no gps device: metrics disabled")

capture = open_camera()
detector = create_detector()
stabilizer = Stabilizer()


def set_velocity(vx, vy):
    speeds = [
        (vx + vy) / WHEEL_RADIUS,
        (vx - vy) / WHEEL_RADIUS,
        (vx - vy) / WHEEL_RADIUS,
        (vx + vy) / WHEEL_RADIUS,
    ]
    for wheel, speed in zip(wheels, speeds):
        wheel.setVelocity(speed)


def velocity_for(direction, level):
    if direction not in DIRECTION:
        return 0.0, 0.0
    dx, dy = DIRECTION[direction]
    speed = SPEED_PER_LEVEL * level
    return dx * speed, dy * speed


def at_goal(position):
    return ((position[0] - GOAL[0]) ** 2 + (position[1] - GOAL[1]) ** 2) ** 0.5 < GOAL_RADIUS


direction = "STOP"
level = 0
step = 0
start_time = None
distance = 0.0
last = None
reached = False

while robot.step(timestep) != -1:
    step += 1
    if step % DETECT_EVERY == 0:
        ok, frame = capture.read()
        if ok:
            frame = cv2.flip(frame, 1)
            result = find_hands(detector, frame)
            draw_hands(frame, result)
            direction, level = stabilizer.update(classify(result))
            cv2.putText(frame, direction + " x" + str(level), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv2.imshow("Gestures", frame)
            cv2.waitKey(1)
    vx, vy = velocity_for(direction, level)
    set_velocity(vx, vy)

    if gps:
        position = gps.getValues()
        if last is not None:
            distance += ((position[0] - last[0]) ** 2 + (position[1] - last[1]) ** 2) ** 0.5
        last = position
        if start_time is None and direction != "STOP":
            start_time = robot.getTime()
        if not reached and start_time is not None and at_goal(position):
            reached = True
            print("Reached goal in %.1f s, path %.2f m" % (robot.getTime() - start_time, distance))
