import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

# Get screen dimensions once at startup
SCREEN_W, SCREEN_H = pyautogui.size()

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
    """Move cursor to where index fingertip (point 8) is pointing."""
    if landmarks is None:
        return
    
    # Landmark 8 is the index fingertip
    x, y, _ = landmarks[8]

    # x and y are 0.0-1.0 — scale up to screen size
    screen_x = int(x * SCREEN_W)
    screen_y = int(y * SCREEN_H)

    pyautogui.moveTo(screen_x, screen_y)