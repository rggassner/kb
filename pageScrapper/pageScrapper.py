#!/usr/bin/python3
from PIL import Image
import pyautogui, random, keyboard, time
time.sleep(5)
for item in range(358):
    im = pyautogui.screenshot(region=[912, 258, 817, 967])
    im.save(str(item)+'.png')
    keyboard.press_and_release('right arrow')
    time.sleep(random.randint(10,20))
