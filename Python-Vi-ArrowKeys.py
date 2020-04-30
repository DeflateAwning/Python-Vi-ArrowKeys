#!/usr/bin/env python3

import keyboard # install with "pip install keyboard"

isDDown = False

def hookCallback(event):
	"""
	Called for every key down/up event.
	@param event a keyboard.KeyboardEvent object
	"""

	print("Got event: " + event.to_json())



def dDownCallback():
	isDDown = True

def dUpCallback():
	isDDown = False





keyboard.on_press_key('d', dDownCallback)
keyboard.on_release_key('d', dUpCallback)

keyboard.hook(hookCallback)




# wait forever
keyboard.wait()