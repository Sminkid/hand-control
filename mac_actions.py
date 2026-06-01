import pyautogui
from config import GESTURE_COOLDOWN

# Prevent pyautogui from throwing if mouse hits screen edge
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # remove default delay between actions

ACTIONS = {
    "swipe_left":  lambda: pyautogui.hotkey("ctrl", "right"),  # next Space
    "swipe_right": lambda: pyautogui.hotkey("ctrl", "left"),   # prev Space
    "swipe_up":    lambda: pyautogui.hotkey("ctrl", "up"),     # Mission Control
    "swipe_down":  lambda: pyautogui.hotkey("ctrl", "down"),   # App Exposé
}

def execute(gesture):
    """Look up the gesture and fire the matching Mac action."""
    action = ACTIONS.get(gesture)
    if action:
        print(f"Gesture detected: {gesture}")
        action()