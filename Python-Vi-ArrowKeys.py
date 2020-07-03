#!/usr/bin/env python3

# Project Homepage: https://github.com/ThePiGuy/Python-Vi-ArrowKeys

import keyboard as kb # install with "pip install keyboard"
import pystray as tray # install with "pip install pystray"
from PIL import Image # install with "pip install wheel pillow"

import sys, string, os

gstate = {						# global state of the system
	"down": set(),				# set of characters currently pressed (set bc there will only ever be a single instance of each)
	"shiftsDown": set(),		# set of shift keys pressed down (left shift, right shift, shift)
	"lastInfo": "",				# stores an information string printed to the user, for caching
	"lastInfoCount": 0,			# comment
	"viTriggeredYet": False,	# whether VI mode has been triggered while d has been pressed (decides where or not to type a 'd' on 'd UP')
	"dSentYet": False,			# whether the 'd' character has been send yet (gets reset on 'd DOWN', and sent when 'd' is typed from either 'UP', 'cards', or 'world' section
	"wasDUppercase": None,		# whether the 'd' character was uppercase or not when pressed
	"capslockState": False,		# True=capslock on, False=capslock off; updated on every keypress

	"icon": None,				# system tray icon
	"enabled": True,			# system tray enabled

}

config = {
	"printDebug": False,			# deployment: False
	"enableSysTray": True,		# deployment: True
	"enableQuickExit": False,	# deployment: False 	# press 'end' key to exit the program (useful for debug only)

	"maps": {					# VI Mappings
		'h': "left",
		'j': "down",
		'k': "up",
		'l': "right"
	},

	"remaps": {					# scan codes/nameL to remap to other characters (primarily number pad)
		82: '0',
		79: '1',
		80: '2',
		81: '3',
		75: '4',
		76: '5',
		77: '6',
		71: '7',
		72: '8',
		73: '9',
		83: '.'
	},

	# List of keys to listen for and apply the system to (prevents issues when they're typed before or after a 'd')
	"hookKeys": list(string.punctuation) + list(string.ascii_lowercase) + ['space', 'end', 'enter', 'backspace'] + list(string.digits),
	"listenKeys": ["shift", "right shift", "left shift"] # just listen to the shift keys for use in the main handler (can only be shifts)
}



config['specials'] = list(config['maps'].keys()) + ['d'] # list of all special characters to remap

def listenCallback(event):
	"""
	Non-supressing listener for certain keys, like the three shift options.
	Used to fix issue where all letters after a D are capitals.
	"""

	nameL = event.name.lower()
	
	## Record which shift was pressed.
	downEvent = False
	if event.event_type == "up":
		if 'shift' in nameL:
			gstate['shiftsDown'].discard(nameL) # use discard to avoid error if not in set
		downEvent = False
	elif event.event_type == "down":
		if 'shift' in nameL:
			gstate['shiftsDown'].add(nameL)
		downEvent = True
	else:
		printf("Unknown event type: " + event.event_type)
		return

	## Print Debug Info
	printDebugInfo("Listen", event)

def hookCallback(event):
	"""
	Called for every key down/up event. This is where the remapping magic happens.
	Everything after this method is just pretty system tray stuff.

	@param event a keyboard.KeyboardEvent object

	Samples of event parameter (with event.to_json()):
		{"event_type": "down", "scan_code": 30, "name": "a", "time": 1588229823.0407975, "is_keypad": false}
		{"event_type": "up", "scan_code": 30, "name": "a", "time": 1588229823.1415234, "is_keypad": false}
	Each attribute/key can be accessed directly with dot notation (ex: event.event_type).
	"""

	nameL = event.name.lower()
	scancode = event.scan_code

	# SECTION 1: Set hotkey for exiting the program
	if (nameL == "end") and config['enableQuickExit']:
		sys.exit()


	# SECTION 2: Record whether this key was pressed (lower case)
	downEvent = False
	if event.event_type == "up":
		gstate['down'].discard(nameL) # use discard to avoid error if not in set
		downEvent = False
	elif event.event_type == "down":
		gstate['down'].add(nameL)
		downEvent = True
	else:
		printf("Unknown event type: " + event.event_type)
		return

	# SECTION 2a: Determine capslock state
	if nameL in string.ascii_lowercase:
		# only update for letters, not numbers nor symbols
		if (event.name in string.ascii_lowercase) and (len(gstate['shiftsDown']) > 0):
			gstate['capslockState'] = True
		elif (event.name in string.ascii_uppercase) and (len(gstate['shiftsDown']) == 0):
			gstate['capslockState'] = True
		else:
			gstate['capslockState'] = False

	# SECTION 3: Pass through normal keys (will require keys down check later)
	if ('d' not in gstate['down']) or (nameL not in config['specials']):
		# if d is not pressed and this isn't for a d
		if downEvent:
			# Do 'cards' fix
			if ('d' in gstate['down']) and (not gstate['dSentYet']):
				kb.press('d') # This should be send, maybe (check back later, if it's an issue)
				gstate['dSentYet'] = True
			
			# Actually send through the character (by character if on the numpad, otherwise by scancode)
			if event.is_keypad and (scancode in config['remaps'].keys()):
				kb.press(config['remaps'][scancode]) # always use the actual number character, regardless of numlock. Used because numlock state is weird
			else:
				kb.press(scancode) # scancode used to avoid issue with 'F' character (to be explicit)
		else:
			# Actually send through the character (by character if on the numpad, otherwise by scancode)
			if event.is_keypad and (scancode in config['remaps'].keys()):
				kb.release(config['remaps'][scancode]) # always use the actual number character, regardless of numlock, used because numlock state is weird
			else:
				kb.release(scancode) # scancode used to avoid issue with 'F' character (to be explicit)


	# SECTION 4: Pass through 'd' based on UP event
	if (nameL == 'd'):
		if downEvent:
			# alternatively we could reset viTriggeredYet=False here
			gstate['dSentYet'] = False # reset to not sent yet
			gstate['wasDUppercase'] = (event.name == 'D')
		else:
			if (not gstate['viTriggeredYet']) and (not gstate['dSentYet']):
				# "Discord" bug fix
				if gstate["wasDUppercase"] and (not gstate['capslockState']):
					# Determine what type of shift to press so that the keyup works later
					if (len(gstate['shiftsDown']) == 0):
						kb.send('shift+d')
					else:
						kb.press(list(gstate['shiftsDown'])[0])
						kb.send('d')
					#kb.press('shift')
					#kb.send('d')
				else:
					kb.send('d')
				gstate['dSentYet'] = True
			gstate['viTriggeredYet'] = False # reset to false


	# SECTION 5: Fix "worl/world" bug
	if any([thisVIKey in gstate['down'] for thisVIKey in config['maps'].keys()]) and (nameL == 'd' and downEvent):
		# If any of the VI keys are currently pressed down, and 'd' is being PRESSED
		kb.send('d') # this might only be a .press, actually; doesn't matter though
		#printf("\nDid 'world' bug fix.")
		gstate['dSentYet'] = True

	# SECTION 6: Perform VI arrow remapping
	if (nameL in config['maps'].keys()) and ('d' in gstate['down']):
		gstate['viTriggeredYet'] = True # VI triggered, no longer type a 'd' on release
		thisSend = config['maps'][nameL]
		if downEvent:
			kb.press(thisSend)
		else:
			kb.release(thisSend)
		#printf("\nSending: " + thisSend)
	
	# Section 7: Print Debug Info
	printDebugInfo("Hook", event)

def printDebugInfo(callbackType, event):
	# SECTION 7: Print Debug Info
	if config['printDebug']:
		info = "\nNew {callbackType} Event: type({type})\tname({scancode} = {name})\tkeysDown({keysDown})\tkeypad({keypad})\tcaps({capslockState})".\
						format(callbackType=callbackType, type=event.event_type, capslockState=gstate['capslockState'], \
	                    name=event.name, scancode=event.scan_code, keysDown=" | ".join(gstate['down']) + " || " + " | ".join(gstate['shiftsDown']), keypad=event.is_keypad)
		if gstate['lastInfo'] != info:
			printf(info, end="")
			gstate['lastInfoCount'] = 0
		elif gstate['lastInfoCount'] < 20: # only print out if it's not already been held for a while
			printf(".", end="")
			gstate['lastInfoCount'] += 1
		gstate['lastInfo'] = info
	

def startHooks():
	"""
	Attaches keyboard hooks, starts the program basically.
	"""

	# Avoid duplicate hooks by removing all hooks first
	#stopHooks()

	# Hook all keys
	# Issues: fails with 'left windows', types a 'd' when shift is pressed, etc.
	#kb.hook(hookCallback, True) # supress characters

	# Hook only letters (and maybe certain other characters)
	for character in config['hookKeys']:
		kb.hook_key(character, hookCallback, True) # supress characters

	for character in config['listenKeys']:
		kb.hook_key(character, listenCallback, False) # don't supress characters

	if config['printDebug']:
		printf("\nAttached {} hooks.".format(len(config['hookKeys'])))

	# wait forever (only useful for when this function is the last thing called, not for system tray)
	if not config["enableSysTray"]:
		kb.wait()


def stopHooks():
	"""
	Removes keyboard hooks, stops listening. Pauses the program.
	"""
	kb.unhook_all() # should do it, but it doesn't

	if config['printDebug']:
		printf("\nStopped all hooks/paused the program.")


def traySetup(icon):
	"""
	Gets called when the system tray icon is created.
	This is run in a separate thread, and its completion is not awaited (it can run forever).
	@param icon presumably the icon itself
	"""
	startHooks()


def trayEnabledChanged(icon):
	""" Gets called when system tray "Enabled" changes state. This must keep track of its own state. """
	gstate['enabled'] = not gstate['enabled'] # toggle it
	if gstate['enabled']:
		startHooks()
	else:
		stopHooks()

def trayRestartButton(icon):
	"""
	Gets called when system tray "Restart" is called. 
	Used because Synergy only allows forwarding of this program's changes if this program is started after Synergy (must be a full start, not just re-Enable).
	Source: https://stackoverflow.com/questions/48129942/python-restart-program/48130340
	"""

	os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


def createSystemTray():
	"""
	Sends the script to run in the system tray.
	This method runs infinitely, until the program is stopped.
	"""

	image = Image.open("icon-64.png")
	menu = tray.Menu(
		tray.MenuItem("VI Arrow Keys", lambda: 1, enabled=False), # inactive item with the program's title
		tray.MenuItem('Enabled', trayEnabledChanged, checked=lambda item: gstate['enabled']),
		#tray.MenuItem('Resume', trayResume)
		tray.MenuItem('Restart', trayRestartButton),
		tray.MenuItem('Quit/Exit', lambda: gstate['icon'].stop()), # just calls icon.stop(), steps the whole program
	)

	gstate['icon'] = tray.Icon("VI Arrow Keys", image, "VI Arrow Keys", menu) # originally stored in "icon", stored globally though
	gstate['icon'].visible = True
	gstate['icon'].run(setup=traySetup) # this creates an infinite loops and runs forever until exit here


def run():
	# Create the system tray icon
	createSystemTray() # never ends


def printf(*args, **kwargs):
	""" A print function that flushes the buffer for immediate feedback. """
	print(*args, **kwargs, flush=True)


if __name__ == "__main__":
	if config['enableSysTray']:
		run()
	else:
		startHooks()
