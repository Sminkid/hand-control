import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from config import MAX_HANDS, DETECTION_CONFIDENCE

class HandTracker:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=MAX_HANDS,
            min_hand_detection_confidence=DETECTION_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):
        """Returns list of (x, y, z) tuples for each landmark, or None."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.detector.detect(mp_image)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            return [(lm.x, lm.y, lm.z) for lm in hand]
        return None

    def draw_skeleton(self, frame, landmarks):
        """Draw all 21 landmarks and connections onto the frame."""
        if landmarks is None:
            return

        h, w, _ = frame.shape

        # Convert normalised coords to pixel positions
        points = [(int(lm[0] * w), int(lm[1] * h)) for lm in landmarks]

        # Finger connections — each tuple is (start_landmark, end_landmark)
        connections = [
            (0,1),(1,2),(2,3),(3,4),         # thumb
            (0,5),(5,6),(6,7),(7,8),          # index
            (0,9),(9,10),(10,11),(11,12),     # middle
            (0,13),(13,14),(14,15),(15,16),   # ring
            (0,17),(17,18),(18,19),(19,20),   # pinky
            (5,9),(9,13),(13,17),             # palm
        ]

        # Draw connections
        for start, end in connections:
            cv2.line(frame, points[start], points[end], (0, 200, 150), 2)

        # Draw each landmark dot and its number
        for i, (x, y) in enumerate(points):
            cv2.circle(frame, (x, y), 6, (255, 255, 255), -1)  # white dot
            cv2.circle(frame, (x, y), 6, (0, 150, 100), 2)     # green ring
            cv2.putText(frame, str(i), (x + 8, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
    def draw_active_zone(self, frame):
        """Draw the active zone boundary on the webcam feed."""
        from mac_actions import X_MIN, X_MAX, Y_MIN, Y_MAX

        h, w, _ = frame.shape

        # Convert normalised zone coords to pixel coords
        x1 = int(X_MIN * w)
        x2 = int(X_MAX * w)
        y1 = int(Y_MIN * h)
        y2 = int(Y_MAX * h)

        # Draw the rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        # Label it
        cv2.putText(frame, "active zone", (x1 + 8, y1 + 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)