#!/usr/bin/env python3

import keyboard # install with "pip install keyboard"

import sys

globalStates = {
	"down": set(), # list of characters currently pressed
	"lastInfo": "", # stores an information string printed to the user, for caching
	"lastInfoCount": 0
}

config = {
	"printDebug": True,

	"maps": { # VI Mappings
		"h": "left",
		"j": "down",
		"k": "up",
		"l": "right"
	}
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

	# Pass through normal keys (will require keys down check later)
	if ('d' not in globalStates["down"]) or (nameL not in config["specials"]):
		if event.event_type == "down":
			keyboard.press(event.scan_code) # scancode used to avoid issue with 'F' character (to be explicit)
		elif event.event_type == "up":
			keyboard.release(event.scan_code)
		else:
			print("Unknown event type: " + event.event_type)


	# Record whether this key was pressed (lower case)
	if event.event_type == "up":
		globalStates["down"].discard(nameL) # use discard to avoid error if not in list
	elif event.event_type == "down":
		globalStates["down"].add(nameL)


	# Perform VI arrow remapping
	if (nameL in config["maps"].keys()) and event.event_type == "down" and ('d' in globalStates["down"]):
		thisSend = config["maps"][nameL]
		# Specifically send a shift if required, but not necessary because it's already recorded as pressed
		# if "shift" in globalStates["down"]:
		# 	# holding shift
		# 	thisSend += "+shift"
		#print("\nSending: " + thisSend)
		keyboard.send(thisSend) # press used instead of send because 'shift' is not applied continually if it is simulated released


	# Print debug info
	if config["printDebug"]:
		info = "\nNew Event: type({type})\tname({name})\t\tkeysDown({keysDown})) ".format(type=event.event_type, name=event.name, keysDown="|".join(globalStates["down"]))
		if globalStates["lastInfo"] != info:
			print(info, end="")
			globalStates["lastInfoCount"] = 0
		elif globalStates["lastInfoCount"] < 20: # only print out if it's not already been held for a while
			print(".", end="")
			globalStates["lastInfoCount"] += 1
		globalStates["lastInfo"] = info


	# Set hotkey for exiting the program
	if (nameL == "end"):
		sys.exit()



keyboard.hook(hookCallback, True) # supress characters

# wait forever
keyboard.wait()