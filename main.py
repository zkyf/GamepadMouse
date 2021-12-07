import pygame
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
import time
import json

config = {
    "mouse_x_axis": 0,
    "mouse_y_axis": 1,
    "scroll_x_axis": 2,
    "scroll_y_axis": 3,

    "move_speed": 2.0,
    "scroll_speed": 2.0,

    "left_key": 0,
    "right_key": 1,
    "screen_keyboard": 2,
    "esc": 3,
    "win_tab": 6,
    "win": 7
}

last_new_config = {}

def translation(x):
    sign = 1
    if x < 0:
        sign = -1
    return sign * x ** 2 * 10 * config["move_speed"]

def scroll(x):
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    y = 0
    if x < 0.1:
        y = 0
    elif x < 0.5:
        y = 1
    elif x < 0.8:
        y = 2
    else:
        y = 3
    return sign * y * config["scroll_speed"]

def pressed(i):
    return joystick.get_button(i) and not last_btns[i]

def released(i):
    return not joystick.get_button(i) and last_btns[i]

pygame.init()
pygame.joystick.init()
done=False

mouse = PyMouse()
keyboard = PyKeyboard()

last_btns = [False] * 64
last_hats = [0, 0]

frame = 0

while (done != True):
    frame = (frame + 1) % 100

    if frame == 0:
        with open('setting.json', 'r') as file:
            new_config = json.load(file)
            if last_new_config != new_config:
                for field in new_config:
                    config[field] = new_config[field]
                print("Settings updated")
                last_new_config = new_config

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    joystick_count = pygame.joystick.get_count()
    for i in range(max(joystick_count, 1)):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        axes = joystick.get_numaxes()

        # Xbox controller
        # X axis: 0 left neg
        # Y axis: 1 up neg
        # X rot: 2 left neg
        # Y rot: 3 up neg
        # LT: 4
        # RT: 5
        # A0 B1 X2 Y3 LB4 RB5 menu7 windows6
        # hats: (x, y)，xy=-1|0|1


        # move mouse
        dx = joystick.get_axis(config["mouse_x_axis"])
        dy = joystick.get_axis(config["mouse_y_axis"])
        if abs(dx) < 0.1:
            dx = 0
        if abs(dy) < 0.1:
            dy = 0
        x, y = mouse.position()
        x = x + translation(dx)
        y = y + translation(dy)

        # left btn
        if pressed(config["left_key"]):
            mouse.press(int(x), int(y))
        if released(config["left_key"]):
            mouse.release(int(x), int(y))

        # right btn
        if pressed(config["right_key"]):
            mouse.press(int(x), int(y), 2)
        if released(config["right_key"]):
            mouse.release(int(x), int(y), 2)

        mouse.move(int(x), int(y))

        if released(config["win"]):
            keyboard.tap_key(keyboard.windows_l_key)

        if released(config["esc"]):
            keyboard.tap_key(keyboard.escape_key)

        if released(config["win_tab"]):
            keyboard.press_key(keyboard.windows_l_key)
            keyboard.press_key(keyboard.tab_key)
            keyboard.release_key(keyboard.tab_key)
            keyboard.release_key(keyboard.windows_l_key)

        if released(config["screen_keyboard"]):
            keyboard.press_key(keyboard.windows_l_key)
            keyboard.press_key(keyboard.control_l_key)
            keyboard.press_key('o')
            keyboard.release_key(keyboard.windows_l_key)
            keyboard.release_key(keyboard.control_l_key)
            keyboard.release_key('o')

        num_btns = joystick.get_numbuttons()
        for i in range(num_btns):
            last_btns[i] = joystick.get_button(i)

        # print(last_btns)
        
        # wheel
        if frame % 5 == 0:
            dsx = joystick.get_axis(config["scroll_x_axis"])
            if abs(dsx) < 0.1:
                dsx = 0
            dsy = joystick.get_axis(config["scroll_y_axis"])
            if abs(dsy) < 0.1:
                dsy = 0
            mouse.scroll(-scroll(dsy), scroll(dsx))

        time.sleep(0.01)
        
