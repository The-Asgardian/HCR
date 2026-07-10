from controller import Robot, Keyboard

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

keyboard = robot.getKeyboard()
keyboard.enable(timestep)


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


def read_keyboard():
    key = keyboard.getKey()
    if key == Keyboard.UP:
        return "FORWARD"
    if key == Keyboard.DOWN:
        return "BACKWARD"
    if key == Keyboard.LEFT:
        return "LEFT"
    if key == Keyboard.RIGHT:
        return "RIGHT"
    return "STOP"


while robot.step(timestep) != -1:
    command = read_keyboard()
    left_speed, right_speed = command_to_speeds(command)
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
