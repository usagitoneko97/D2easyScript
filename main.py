import pythoncom
import pyHook
from send_keys import PressKey, ReleaseKey
import pyautogui
import time
from PIL import ImageGrab
import numpy as np
import cv2
import win32api
import win32con

# List of scan code
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
Q = 0x10
W = 0x11
E = 0x12
R = 0x13
D = 0x20
F = 0x21
Z = 0x2C
X = 0x2D
C = 0x2E
V = 0x2F
B = 0x30
P = 0x19
TAB = 0x0F
SPACE = 0x39

SKILL_1 = Q
SKILL_2 = W
SKILL_3 = E
SKILL_4 = R
SKILL_5 = D
SKILL_6 = F

ITEM_1 = Z
ITEM_2 = X
ITEM_3 = C
ITEM_4 = V
ITEM_5 = B
ITEM_6 = SPACE


def OnKeyboardEvent(event):
    print(event.Key)
    if event.Key == 'Subtract':
        poof()
    elif event.Key == 'Add':
        pyautogui.moveTo(1125, 968)
        pyautogui.dragTo(1125, 929, 0.1001, button='left')
    elif event.Key == 'Multiply':
        #demonstration
        alacrity()
        pressKeyboard(SKILL_1)
        pressKeyboard(SKILL_1)
        pressKeyboard(SKILL_1)
        pressKeyboard(SKILL_4)
        time.sleep(0.2)

        x, y = get_hero_loc()
        offset = calculate_hero_offset(x)
        pressKeyboard(D)
        prevs_time = time.time()
        mouse_click_hero(x+offset, y)
        print('2nd loop took {} seconds'.format(time.time() - prevs_time))
        # cv2.imshow('window', image)

    elif event.Key == 'Numpad0':
        current_time = time.time()
        x, y = get_hero_loc()
        hero_offset = calculate_hero_offset(x)
        mouse_click_hero(x+hero_offset, y)

        print('numpad0 loop took {} seconds'.format(time.time() - current_time))

    elif event.Key=='P':
        x, y = get_hero_loc()
        # pyautogui.moveTo()
        pressKeyboard(C)
        pyautogui.click(x, y + 40)
        lina()

    # return True to pass the event to other handlers
    return True


def calculate_hero_offset(x):
    """
    calculate hero position relative to health bar
    :param x: x coordinate
    :return: hero offset
    """
    x_without_padding = x - 180
    print("x without padding = ", x_without_padding)
    if x_without_padding < 600:
        factor = 45-((x_without_padding / 800) * 45) + 45
        hero_offset = factor - ((x_without_padding / 800) * factor)
    elif x_without_padding > 1000:
        factor = (((x_without_padding-800) / 800) * 45) + 45
        hero_offset = -(((x_without_padding - 800) / 800) * factor)
    else:
        factor = 0
        hero_offset = 0
    print("factor = ", factor)
    print("hero offset = ", hero_offset)
    return int(hero_offset)


def mouse_click_hero(x, y):
    win32api.SetCursorPos((x, y+60))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y+60, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y+60, 0, 0)


def get_hero_loc():
    # get the screen, filter out every color except red, and find contours
    # TODO performance need to test (check the time)
    last_time = time.time()
    printscreen = np.array(ImageGrab.grab(bbox=(180, 90, 1780, 990)))  # 1600x900 in 1920x1080 with equal padding
    lower = np.array([170, 40, 0])
    upper = np.array([243, 60, 0])
    shape_mask = cv2.inRange(printscreen, lower, upper)
    image, contours, hierarchy = cv2.findContours(shape_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for i in contours:
    #     np.sort(i)
    cv2.imshow('window', image)
    previous_max = 0
    previous_min = 1900
    print(contours)
    for element in contours:
        for contours_num in element:
            if contours_num[0, 0] > previous_max:
                previous_max = contours_num[0, 0]
            if contours_num[0, 0] < previous_min:
                previous_min = contours_num[0, 0]

    print("previous max = ", previous_max)
    print("previous min = ", previous_min)
    herobar_middle = previous_min + 40
    y_coordinate = contours[0][0]

    print('loop took {} seconds'.format(time.time() - last_time))
    return herobar_middle+180, y_coordinate.flat[1]+90   # 180 and 90 is padding


def alacrity():
    pressKeyboard(W)
    pressKeyboard(W)
    pressKeyboard(E)
    pressKeyboard(R)
    time.sleep(0.2)
    pressKeyboard(D)
    pressKeyboard(D)
    time.sleep(0.2)
    pressKeyboard(W)
    pressKeyboard(W)
    pressKeyboard(W)

def poof():
    pressKeyboard(TAB)
    pressKeyboard(W)
    pressKeyboard(TAB)
    pressKeyboard(W)
    pressKeyboard(TAB)
    pressKeyboard(W)
    pressKeyboard(TAB)
    # pressKeyboard(W)
    # pressKeyboard(TAB)

def lina():
    time.sleep(1.7)
    pressKeyboard(W)
    pyautogui.click()
    time.sleep(0.2)
    pressKeyboard(Q)
    pyautogui.click()

def earthSpiritStun():
    pressKeyboard(D)
    pressKeyboard(D)
    PressKey(Q)

def pressKeyboard(vkCode):
    PressKey(vkCode)
    ReleaseKey(vkCode)

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse event
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
