import cv2

from camera import open_camera
from hands import create_detector, find_hands, draw_hands

WRIST = 0
INDEX_MCP = 5
INDEX_PIP = 6
INDEX_TIP = 8
FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]


def distance(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def fingers_extended(landmarks):
    count = 0
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        if distance(landmarks[tip], landmarks[WRIST]) > distance(landmarks[pip], landmarks[WRIST]):
            count += 1
    return count


def index_extended(landmarks):
    return distance(landmarks[INDEX_TIP], landmarks[WRIST]) > distance(landmarks[INDEX_PIP], landmarks[WRIST])


def index_direction(landmarks):
    dx = landmarks[INDEX_TIP].x - landmarks[INDEX_MCP].x
    dy = landmarks[INDEX_TIP].y - landmarks[INDEX_MCP].y
    if abs(dx) > abs(dy):
        return "WEST" if dx < 0 else "EAST"
    return "NORTH" if dy < 0 else "SOUTH"


def classify(result):
    if not result.hand_landmarks:
        return ("STOP", 0)
    landmarks = result.hand_landmarks[0]
    if not index_extended(landmarks):
        return ("STOP", 0)
    return (index_direction(landmarks), fingers_extended(landmarks))


class Stabilizer:
    def __init__(self, window=4):
        self.window = window
        self.stable = ("STOP", 0)
        self.candidate = ("STOP", 0)
        self.count = 0

    def update(self, command):
        if command == self.candidate:
            self.count += 1
        else:
            self.candidate = command
            self.count = 1
        if self.count >= self.window:
            self.stable = command
        return self.stable


def main():
    capture = open_camera()
    detector = create_detector()
    stabilizer = Stabilizer()
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        result = find_hands(detector, frame)
        draw_hands(frame, result)
        direction, level = stabilizer.update(classify(result))
        cv2.putText(frame, direction + " x" + str(level), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.imshow("Gestures", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
