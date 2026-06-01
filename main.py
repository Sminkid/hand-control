import cv2
from hand_tracker import HandTracker
from gesture_engine import GestureEngine
from mac_actions import execute, move_cursor
from config import CAMERA_INDEX, FLIP_FRAME, SHOW_DEBUG

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    tracker = HandTracker()
    engine = GestureEngine()

    print("Hand gesture control running — press Q to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found")
            break

        if FLIP_FRAME:
            frame = cv2.flip(frame, 1)

        landmarks = tracker.get_landmarks(frame)
        gesture = engine.update(landmarks)
        move_cursor(landmarks)

        if gesture:
            execute(gesture)

        if SHOW_DEBUG:
            tracker.draw_skeleton(frame, landmarks)
            tracker.draw_active_zone(frame)
            label = gesture if gesture else "watching..."
            cv2.putText(frame, label, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Hand Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()