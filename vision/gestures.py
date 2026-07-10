import cv2

from camera import open_camera
from hands import create_detector, find_hands, draw_hands

FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]


def count_fingers(landmarks):
    count = 0
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        if landmarks[tip].y < landmarks[pip].y:
            count += 1
    return count


def command_for_count(fingers):
    if fingers == 1:
        return "FORWARD"
    if fingers == 2:
        return "LEFT"
    if fingers == 3:
        return "RIGHT"
    if fingers == 4:
        return "BACKWARD"
    return "STOP"


def classify(result):
    if not result.hand_landmarks:
        return "STOP"
    return command_for_count(count_fingers(result.hand_landmarks[0]))


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
        command = classify(result)
        cv2.putText(frame, command, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.imshow("Gestures", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
