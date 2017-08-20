from pynput.keyboard import Key, Controller
from pynput import keyboard
import pyautogui
keyboard1 = Controller()

def on_press(key):
    try:
        if key.char == '+':
            pyautogui.moveTo(1120, 968)
            pyautogui.dragTo(1112, 929, 0.1001, button='left')
        elif key.char == '-':
            keyboard1.press(Key.space)
            keyboard1.release(Key.space)

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()