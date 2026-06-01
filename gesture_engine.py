import time
from collections import deque
from config import HISTORY_LENGTH, SWIPE_SPEED_THRESHOLD, GESTURE_COOLDOWN

# Landmark index constants — named so the code reads like english
WRIST       = 0
THUMB_TIP   = 4
INDEX_TIP   = 8
MIDDLE_TIP  = 12
INDEX_MCP   = 5  # index knuckle

class GestureEngine:
    def __init__(self):
        self.history = deque(maxlen=HISTORY_LENGTH)
        self.last_gesture_time = 0

    def update(self, landmarks):
        """Call every frame. Returns a gesture string or None."""
        if landmarks is None:
            self.history.clear()
            return None

        wrist_x = landmarks[WRIST][0]
        wrist_y = landmarks[WRIST][1]
        self.history.append((wrist_x, wrist_y, time.time()))

        # Still in cooldown from last gesture
        if time.time() - self.last_gesture_time < GESTURE_COOLDOWN:
            return None

        gesture = self._classify()
        if gesture:
            self.last_gesture_time = time.time()
            self.history.clear()

        return gesture

    def _classify(self):
        """Look at the movement history and decide what gesture was made."""
        if len(self.history) < 10:
            return None

        oldest = self.history[0]
        newest = self.history[-1]

        dx = newest[0] - oldest[0]  # positive = moved right
        dy = newest[1] - oldest[1]  # positive = moved down
        dt = newest[2] - oldest[2]  # time elapsed in seconds

        speed = (dx**2 + dy**2) ** 0.5 / max(dt, 0.001)

        if speed < SWIPE_SPEED_THRESHOLD:
            return None

        # Check which axis had more movement
        if abs(dx) > abs(dy) * 1.5:
            return "swipe_right" if dx > 0 else "swipe_left"
        elif abs(dy) > abs(dx) * 1.5:
            return "swipe_down" if dy > 0 else "swipe_up"

        return None