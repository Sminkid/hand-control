import time
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

SCREEN_W, SCREEN_H = pyautogui.size()

X_MIN, X_MAX = 0.1, 0.9
Y_MIN, Y_MAX = 0.1, 0.9

PINCH_THRESHOLD = 0.05

ACTIONS = {
    "swipe_left":  lambda: pyautogui.hotkey("ctrl", "right"),
    "swipe_right": lambda: pyautogui.hotkey("ctrl", "left"),
    "swipe_up":    lambda: pyautogui.hotkey("ctrl", "up"),
    "swipe_down":  lambda: pyautogui.hotkey("ctrl", "down"),
}

# Track pinch state
is_pinching = False

def execute(gesture):
    action = ACTIONS.get(gesture)
    if action:
        print(f"Gesture detected: {gesture}")
        action()

def move_cursor(landmarks):
    if landmarks is None:
        return

    # Use palm centre instead of index tip — average of the 4 knuckles
    # Points 5, 9, 13, 17 are the base knuckles of each finger
    palm_x = (landmarks[5][0] + landmarks[9][0] + landmarks[13][0] + landmarks[17][0]) / 4
    palm_y = (landmarks[5][1] + landmarks[9][1] + landmarks[13][1] + landmarks[17][1]) / 4

    palm_x = max(X_MIN, min(X_MAX, palm_x))
    palm_y = max(Y_MIN, min(Y_MAX, palm_y))

    screen_x = int((palm_x - X_MIN) / (X_MAX - X_MIN) * SCREEN_W)
    screen_y = int((palm_y - Y_MIN) / (Y_MAX - Y_MIN) * SCREEN_H)

    pyautogui.moveTo(screen_x, screen_y)

def check_pinch(landmarks):
    """Hold mouse button down while pinching, release when open."""
    global is_pinching

    if landmarks is None:
        if is_pinching:
            pyautogui.mouseUp()
            is_pinching = False
        return

    thumb = landmarks[4]
    index = landmarks[8]

    dist = ((thumb[0] - index[0])**2 + (thumb[1] - index[1])**2) ** 0.5

    if dist < PINCH_THRESHOLD and not is_pinching:
        print("Pinch — mouse down")
        pyautogui.mouseDown()
        is_pinching = True

    elif dist >= PINCH_THRESHOLD and is_pinching:
        print("Release — mouse up")
        pyautogui.mouseUp()
        is_pinching = False