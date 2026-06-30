import time
from collections import deque
from config import HISTORY_LENGTH, SWIPE_SPEED_THRESHOLD, GESTURE_COOLDOWN

WRIST       = 0
THUMB_TIP   = 4
INDEX_TIP   = 8
MIDDLE_TIP  = 12
INDEX_MCP   = 5

opposites = {
    "swipe_left": "swipe_right",
    "swipe_right": "swipe_left"
}

class GestureEngine:
    def __init__(self):
        self.history = deque(maxlen=HISTORY_LENGTH)
        self.last_gesture_time = 0
        self.last_gesture_direction = None

    def update(self, landmarks):
        """Call every frame. Returns a gesture string or None."""
        if landmarks is None:
            self.history.clear()
            return None

        middle_x = landmarks[MIDDLE_TIP][0]
        middle_y = landmarks[MIDDLE_TIP][1]
        self.history.append((middle_x, middle_y, time.time()))

        if time.time() - self.last_gesture_time < GESTURE_COOLDOWN:
            return None

        gesture = self._classify()
        if gesture:
            self.last_gesture_time = time.time()
            self.last_gesture_direction = gesture
            self.history.clear()

        return gesture

    def _classify(self):
        if len(self.history) < 10:
            return None

        oldest = self.history[0]
        newest = self.history[-1]

        dx = newest[0] - oldest[0]
        dy = newest[1] - oldest[1]
        dt = newest[2] - oldest[2]

        speed = (dx**2 + dy**2) ** 0.5 / max(dt, 0.001)

        if speed < SWIPE_SPEED_THRESHOLD:
            return None

        if abs(dx) > 0.15:
            return "swipe_right" if dx > 0 else "swipe_left"

        return None