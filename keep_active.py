# keep_active.py

"""
Little script to run when using google colab to keep
it from disconnecting, just presses the up and down arrows
every once and a while to make it seem like I am still
interacting with it
"""

from pyautogui import press, typewrite, hotkey
import time
from random import shuffle

array = ["up", "down"]

while True:
	print("Pressing")
	shuffle(array)
	time.sleep(10)
	press(array[0])
	press(array[1])
