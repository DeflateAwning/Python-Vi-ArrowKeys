#!/usr/bin/env python3

import keyboard # install with "pip install keyboard"

import sys

gstate = { # global state of the system
	"down": set(), # set of characters currently pressed (set bc there will only ever be a single instance of each)
	"lastInfo": "", # stores an information string printed to the user, for caching
	"lastInfoCount": 0,
	"viTriggeredYet": False # whether VI mode has been triggered while d has been pressed (decides where or not to type a 'd' on 'd UP')
}

config = {
	"printDebug": True,

	"maps": { # VI Mappings
		"h": "left",
		"j": "down",
		"k": "up",
		"l": "right"
	},

	"enableQuickExit": True # press 'end' key to exit the program
}

config["specials"] = list(config["maps"].keys()) + ["d"] # list of all special characters to remap



def hookCallback(event):
	"""
	Called for every key down/up event.
	@param event a keyboard.KeyboardEvent object

	Samples of event parameter (with event.to_json()):
		{"event_type": "down", "scan_code": 30, "name": "a", "time": 1588229823.0407975, "is_keypad": false}
		{"event_type": "up", "scan_code": 30, "name": "a", "time": 1588229823.1415234, "is_keypad": false}
	Each attribute/key can be accessed directly with dot notation (ex: event.event_type).
	"""

	nameL = event.name.lower()

	# Set hotkey for exiting the program
	if (nameL == "end") and config["enableQuickExit"]:
		sys.exit()

	# Record whether this key was pressed (lower case)
	if event.event_type == "up":
		gstate["down"].discard(nameL) # use discard to avoid error if not in set
	elif event.event_type == "down":
		gstate["down"].add(nameL)


	# Pass through normal keys (will require keys down check later)
	if ('d' not in gstate["down"]) or (nameL not in config["specials"]):
		# if d is not pressed and this isn't for a d
		if event.event_type == "down":
			keyboard.press(event.scan_code) # scancode used to avoid issue with 'F' character (to be explicit)
		elif event.event_type == "up":
			keyboard.release(event.scan_code)
		else:
			print("Unknown event type: " + event.event_type)


	# Pass through 'd' based on UP event
	if (nameL == "d"):
		if event.event_type == "up":
			if not gstate["viTriggeredYet"]:
				keyboard.send('d')
			gstate["viTriggeredYet"] = False # reset to false

		elif event.event_type == "down":
			pass # nothing goes here, alternatively we could reset viTriggeredYet=False here

	# Fix "worl/world" bug
	if any([thisVIKey in gstate["down"] for thisVIKey in config["maps"].keys()]) and (nameL == 'd' and event.event_type == 'down'):
		# If any of the VI keys are currently pressed down, and 'd' is being PRESSED
		keyboard.send('d') # this might only be a .press, actually; doesn't matter though
		print("\nDid 'world' bug fix.")

	# Perform VI arrow remapping
	if (nameL in config["maps"].keys()) and ('d' in gstate["down"]):
		gstate["viTriggeredYet"] = True # VI triggered, no longer type a d on release
		thisSend = config["maps"][nameL]
		if event.event_type == "down":
			keyboard.press(thisSend)
		elif event.event_type == "up":
			keyboard.release(thisSend)
		#print("\nSending: " + thisSend)


	# Print debug info
	if config["printDebug"]:
		info = "\nNew Event: type({type})\tname({name})\t\tkeysDown({keysDown})) ".format(type=event.event_type, name=event.name, keysDown="|".join(gstate["down"]))
		if gstate["lastInfo"] != info:
			print(info, end="")
			gstate["lastInfoCount"] = 0
		elif gstate["lastInfoCount"] < 20: # only print out if it's not already been held for a while
			print(".", end="")
			gstate["lastInfoCount"] += 1
		gstate["lastInfo"] = info





keyboard.hook(hookCallback, True) # supress characters

# wait forever
keyboard.wait()