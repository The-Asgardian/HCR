# Gesture-Controlled Simulated Robot

Drive a simulated robot through a maze using hand gestures from a webcam. Hand
landmarks are detected with MediaPipe, turned into a direction and speed, and
sent to a holonomic KUKA youBot in the Webots simulator.

## Requirements

- Webots R2025a
- Python 3.11 (MediaPipe does not support newer versions)
- A webcam

## Setup

From the project root:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Point Webots at this environment so the controller can import the vision
libraries: Tools > Preferences > Python command, set it to the full path of
`.venv\Scripts\python.exe`.

## Run

1. Open `worlds/maze.wbt` in Webots (File > Open World). The first open
   downloads the robot and object models, so an internet connection is needed
   once.
2. The simulation starts the controller automatically and a camera window
   opens.
3. Show gestures to drive the robot from the start corner to the red goal.

## Controls

- Point index finger up, right, down or left: move North, East, South or West
- 1 to 4 extended fingers: speed level
- Fist or no hand: stop

The camera view is mirrored and the simulator view is top-down with North up, so
you point in the direction you want the robot to travel.

## Project structure

```
controllers/gesture_controller/   Webots controller (vision + driving)
vision/camera.py                  webcam capture
vision/hands.py                   MediaPipe hand landmarks
vision/gestures.py                gesture classifier and smoothing
vision/models/                    MediaPipe hand landmark model
worlds/maze.wbt                   the maze world
requirements.txt                  Python dependencies
```

## Testing the vision alone

The gesture pipeline runs without Webots:

```
.venv\Scripts\python.exe vision\gestures.py
```

A window shows the detected direction and speed level. Press `q` to quit.
