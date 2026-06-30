# All tunable values in one place — tweak these as you test

CAMERA_INDEX = 0          # 0 = built-in webcam
FLIP_FRAME = True         # mirror mode (more intuitive)
SHOW_DEBUG = True         # show webcam window while running

# Hand tracking
MAX_HANDS = 1
DETECTION_CONFIDENCE = 0.7

# Gesture engine
HISTORY_LENGTH = 20       # how many frames to track
SWIPE_SPEED_THRESHOLD = 0.4   # minimum speed to count as a swipe
GESTURE_COOLDOWN = 1.5   # seconds before next gesture fires

