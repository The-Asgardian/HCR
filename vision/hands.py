import os

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

from camera import open_camera

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "hand_landmarker.task")


def create_detector():
    options = vision.HandLandmarkerOptions(
        base_options=mp_tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1,
    )
    return vision.HandLandmarker.create_from_options(options)


def find_hands(detector, frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    return detector.detect(image)


def draw_hands(frame, result):
    height, width = frame.shape[:2]
    for hand in result.hand_landmarks:
        for landmark in hand:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)


def main():
    capture = open_camera()
    detector = create_detector()
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        result = find_hands(detector, frame)
        draw_hands(frame, result)
        cv2.imshow("Hands", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
