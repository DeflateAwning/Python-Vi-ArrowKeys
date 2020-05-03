#!/usr/bin/env python3

# Project Homepage: https://github.com/ThePiGuy/Python-Vi-ArrowKeys

# import keyboard # install with "pip install keyboard"
from pynput import keyboard # install with "pip install pynput"
import pystray as tray # install with "pip install pystray"
from PIL import Image # install with "pip install wheel pillow"

import sys, string, time

gstate = { # global state of the system
	"down": set(), # set of characters currently pressed (set bc there will only ever be a single instance of each)
	"lastInfo": "", # stores an information string printed to the user, for caching
	"lastInfoCount": 0,
	"viTriggeredYet": False, # whether VI mode has been triggered while d has been pressed (decides where or not to type a 'd' on 'd UP')
	"dSentYet": False, # whether the 'd' character has been send yet (gets reset on 'd DOWN', and sent when 'd' is typed from either 'UP', 'cards', or 'world' section

	"icon": None, # system tray icon
	"enabled": True, # system tray enabled

	"listener": None, # keyboard listener
	"controller": None, # keyboard controller
}

config = {
	"printDebug": True,
	"enableSysTray": False,

	"maps": { # VI Mappings
		"h": "left",
		"j": "down",
		"k": "up",
		"l": "right"
	},

	"enableQuickExit": True # press 'end' key to exit the program (useful for debug only), doesn't work for systray
}

config["specials"] = list(config["maps"].keys()) + ["d"] # list of all special characters to remap

# List of keys to listen for and apply the system to (prevents issues when they're typed before or after a 'd')
config["hookKeys"] = list(string.punctuation) + list(string.ascii_lowercase) + list(string.digits) + ['space', 'end', 'enter', 'backspace']

def sendStroke(stroke, strokeType):
	"""
	Sends a keystroke. This method says it happens fast, but it appears to take a very long time, and doesn't work/is inefficient.
	@param stroke The key to press
	@param strokeType "press", "release", "send"/"type"
	"""
	startTime = time.time()
	stopHooks() # cancel listening while sending the stroke
	
	if strokeType == "press":
		gstate["controller"].press(stroke)
	elif strokeType == "release":
		gstate["controller"].release(stroke)
	elif strokeType == "send" or strokeType == "type":
		gstate["controller"].type(stroke)
	else:
		raise Exception("Invalid strokeType: " + strokeType)

	startHooks()
	print("\tSend Stroke Time: {}ms".format((time.time()-startTime)/1000))

def hookCallback(key, direction):
	"""
	Called for every key down/up event. This is where the remapping magic happens.
	Everything after this method is just pretty system tray stuff.

	@param key a keyboard.KeyCode object (never a string, turns out)
	@param direction "up" or "down"

	"""

	# convert key to lower case, if it's not a fancy key
	if type(key) == str: # this case is currently never reached, need to perform a different check
		nameL = key.lower()
		print("Lowercase: " + str(key))
	else:
		nameL = key

	breakpoint()

	# SECTION 1: Set hotkey for exiting the program
	if (key == keyboard.Key.end) and config["enableQuickExit"]:
		if config["printDebug"]:
			print("\nQuitting. Press CTRL+C to really quit.")
		return False # stop the handler/quit

	# SECTION 2: Record whether this key was pressed (lower case)
	if direction == "up":
		gstate["down"].discard(nameL) # use discard to avoid error if not in set
	elif direction == "down":
		gstate["down"].add(nameL)


	# # SECTION 3: Pass through normal keys (will require keys down check later)
	# if ('d' not in gstate["down"]) or (nameL not in config["specials"]):
	# 	# if d is not pressed and this isn't for a d
	# 	if direction == "down":
	# 		# Do 'cards' fix
	# 		if ('d' in gstate["down"]) and (not gstate["dSentYet"]):
	# 			sendStroke('d', "press")
	# 			gstate["dSentYet"] = True
			
	# 		sendStroke(key, "press") # scancode used to avoid issue with 'F' character (to be explicit)
	# 	elif direction == "up":
	# 		sendStroke(key, "release")
	# 	else:
	# 		print("Unknown event type: " + direction)


	# # SECTION 4: Pass through 'd' based on UP event
	# if (nameL == "d"):
	# 	if direction == "up":
	# 		if (not gstate["viTriggeredYet"]) and (not gstate["dSentYet"]):
	# 			sendStroke('d', "send")
	# 			gstate["dSentYet"] = True
	# 		gstate["viTriggeredYet"] = False # reset to false

	# 	elif direction == "down":
	# 		# alternatively we could reset viTriggeredYet=False here
	# 		gstate["dSentYet"] = False # reset to not sent yet


	# # SECTION 5: Fix "worl/world" bug
	# if any([thisVIKey in gstate["down"] for thisVIKey in config["maps"].keys()]) and (nameL == 'd' and direction == 'down'):
	# 	# If any of the VI keys are currently pressed down, and 'd' is being PRESSED
	# 	sendStroke('d', "send") # this might only be a .press, actually; doesn't matter though
	# 	#print("\nDid 'world' bug fix.")
	# 	gstate["dSentYet"] = True

	# SECTION 6: Perform VI arrow remapping
	if (nameL in config["maps"].keys()) and ('d' in gstate["down"]):
		gstate["viTriggeredYet"] = True # VI triggered, no longer type a 'd' on release
		thisSend = config["maps"][nameL]
		if direction == "down":
			sendStroke(thisSend, "press")
		elif direction == "up":
			sendStroke(thisSend, "release")
		#print("\nSending: " + thisSend)


	# SECTION 7: Print debug info
	if config["printDebug"]:
		info = "\nNew Event: dir({direction})\tkey|nameL({key}|{nameL})\t\tkeysDown({keysDown}) ".format(direction=direction, key=key, nameL=nameL, keysDown=" , ".join([str(i) for i in gstate["down"]]))
		if gstate["lastInfo"] != info:
			print(info, end="")
			gstate["lastInfoCount"] = 0
		elif gstate["lastInfoCount"] < 20: # only print out if it's not already been held for a while
			print(".", end="")
			gstate["lastInfoCount"] += 1
		gstate["lastInfo"] = info

	return True # make it keep running

def startHooks(waitAtEnd = False):
	"""
	Attaches keyboard hooks, starts the program basically.
	"""

	# create the controller
	if gstate["controller"] is None:
		gstate["controller"] = keyboard.Controller()

	gstate["listener"] = keyboard.Listener(
		on_press= lambda key: hookCallback(key, "down"),
		on_release= lambda key: hookCallback(key, "up"),
		supress=True)

	gstate["listener"].start()

	if config["printDebug"]:
		print("\nAttached {} hooks.".format(len(config["hookKeys"])))

	# wait forever (only useful for when this function is the last thing called, not for system tray)
	if waitAtEnd:
		while 1:
			pass

def stopHooks():
	"""
	Removes keyboard hooks, stops listening. Pauses the program.
	"""

	gstate["listener"].stop()

	if config["printDebug"]:
		print("\nStopped all hooks/paused the program.")

def traySetup(icon):
	"""
	Gets called when the system tray icon is created.
	This is run in a separate thread, and its completion is not awaited (it can run forever).
	@param icon presumably the icon itself
	"""
	startHooks()

def trayEnabledChanged(icon):
	""" Gets called when system tray "Enabled" changes state. This must keep track of its own state. """
	gstate["enabled"] = not gstate["enabled"] # toggle it
	if gstate["enabled"]:
		startHooks()
	else:
		stopHooks()


def createSystemTray():
	"""
	Sends the script to run in the system tray.
	This method runs infinitely, until the program is stopped.
	"""

	image = Image.open("icon-64.png")
	menu = tray.Menu(
		tray.MenuItem("VI Arrow Keys", lambda: 1, enabled=False), # inactive item with the program's title
		tray.MenuItem('Enabled', trayEnabledChanged, checked=lambda item: gstate["enabled"]),
		#tray.MenuItem('Resume', trayResume)
		tray.MenuItem('Quit/Exit', lambda: gstate["icon"].stop()), # just calls icon.stop(), steps the whole program
	)

	gstate["icon"] = tray.Icon("VI Arrow Keys", image, "VI Arrow Keys", menu) # originally stored in "icon", stored globally though
	gstate["icon"].visible = True
	gstate["icon"].run(setup=traySetup) # this creates an infinite loops and runs forever until exit here


def run():
	# Create the system tray icon
	createSystemTray() # never ends

if __name__ == "__main__":
	if config["enableSysTray"]:
		run()
	else:
		startHooks(True)