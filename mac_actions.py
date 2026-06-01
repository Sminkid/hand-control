import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

SCREEN_W, SCREEN_H = pyautogui.size()

# Define the active zone — the portion of the webcam frame you actually use
# 0.2 means ignore the outer 20% on each side
X_MIN, X_MAX = 0.3, 0.7
Y_MIN, Y_MAX = 0.2, 0.8

ACTIONS = {
    "swipe_left":  lambda: pyautogui.hotkey("ctrl", "right"),
    "swipe_right": lambda: pyautogui.hotkey("ctrl", "left"),
    "swipe_up":    lambda: pyautogui.hotkey("ctrl", "up"),
    "swipe_down":  lambda: pyautogui.hotkey("ctrl", "down"),
}

def execute(gesture):
    action = ACTIONS.get(gesture)
    if action:
        print(f"Gesture detected: {gesture}")
        action()

def move_cursor(landmarks):
    """Move cursor based on index fingertip position within the active zone."""
    if landmarks is None:
        return

    x, y, _ = landmarks[8]

    # Clamp to active zone
    x = max(X_MIN, min(X_MAX, x))
    y = max(Y_MIN, min(Y_MAX, y))

    # Remap active zone to full screen
    screen_x = int((x - X_MIN) / (X_MAX - X_MIN) * SCREEN_W)
    screen_y = int((y - Y_MIN) / (Y_MAX - Y_MIN) * SCREEN_H)

    pyautogui.moveTo(screen_x, screen_y)