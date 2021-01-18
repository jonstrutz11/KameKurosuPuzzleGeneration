"""Simulate all keyboard commands required to generate crosswords using
クロスワード　ギバー. This allows us to create roughly 4 crossword puzzles per
minute automatically.

The destination folder must be manually set in クロスワード　ギバー before
running this module.
"""


import time

from pynput.keyboard import Controller, Key


keyboard = Controller()

time.sleep(5)

for i in range(1, 101):  # Filename will be i.xwj
    keyboard.press(Key.ctrl_l)
    time.sleep(0.1)
    keyboard.press('g')
    time.sleep(0.1)
    keyboard.release(Key.ctrl_l)
    keyboard.release('g')
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(3)
    keyboard.press('r')
    time.sleep(3)
    keyboard.press('r')
    time.sleep(10)
    keyboard.release('r')
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(0.5)
    keyboard.press(Key.ctrl_l)
    time.sleep(0.1)
    keyboard.press('s')
    time.sleep(0.1)
    keyboard.release(Key.ctrl_l)
    keyboard.release('s')
    time.sleep(1)
    for char in str(i):
        keyboard.press(char)
        time.sleep(0.1)
        keyboard.release(char)
        time.sleep(0.1)
    keyboard.press(Key.tab)
    time.sleep(0.1)
    keyboard.release(Key.tab)
    time.sleep(0.1)
    keyboard.press(Key.down)
    time.sleep(0.1)
    keyboard.press(Key.down)
    time.sleep(0.1)
    keyboard.release(Key.down)
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(1)
    keyboard.press(Key.tab)
    time.sleep(0.1)
    keyboard.press(Key.tab)
    time.sleep(0.1)
    keyboard.release(Key.tab)
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(1)
