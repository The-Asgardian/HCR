import cv2

CAMERA_INDEX = 0


def open_camera(index=CAMERA_INDEX):
    capture = cv2.VideoCapture(index)
    if not capture.isOpened():
        raise RuntimeError("Could not open camera")
    return capture


def main():
    capture = open_camera()
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
