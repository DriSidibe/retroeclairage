#! python3
import pyautogui
import time
import screen_brightness_control as sbc
import os
import keyboard
from pynput import keyboard
import threading
import json

key_pressed = False


# thread 2
def key_board():
    global key_pressed
    try:
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.esc:
                    break
                else:
                    key_pressed = True
                    print('Received event {}'.format(event))
    except Exception as exc:
        print(exc)
    input()

# thread 1
def mouse():
    global key_pressed
    delay = 300
    wait_time = 0
    x_old, y_old = 0, 0
    current_brightness = int(sbc.get_brightness()[0])
    activate = False
    lock = False
    try:
        try:
            with open('retroeclairage_settings.json') as config_file:
                data = json.load(config_file)
                delay = int(data.get('delay'))
        except:
            print("Erreur: lecture du fichier de configuration")
        while True:
            time.sleep(1)
            x, y = pyautogui.position()
            if x_old != x or y_old != y or key_pressed:
                x_old, y_old = x, y
                wait_time = 0
                key_pressed = False
                if activate:
                    print(current_brightness)
                    sbc.set_brightness(current_brightness)
                activate = False
            else:
                wait_time += 1
                print(wait_time)
            if wait_time >= delay and wait_time <= delay + 2:
                if not activate:
                    current_brightness = int(sbc.get_brightness()[0])
                    sbc.set_brightness(0)
                activate = True
                lock = False
            if wait_time >= delay + 60:
                if not lock:
                    os.system('Rundll32.exe user32.dll,LockWorkStation')
                    not_lock = True
    except Exception as exc:
        print(exc)
    input()


# set up threads
th1 = threading.Thread(target=mouse)
th2 = threading.Thread(target=key_board)
th1.start()
th2.start()
th1.join()
th2.join()
