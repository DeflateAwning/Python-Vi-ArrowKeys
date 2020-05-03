
# Test.py

from pynput import keyboard

def hookCallback(key, direction):
	print("key({key}), state({direction})".format(key=key, direction=direction))

	return True

listener = keyboard.Listener(
	on_press= lambda key: hookCallback(key, "down"),
	on_release= lambda key: hookCallback(key, "up"),
	supress=True)

listener.start()

while 1:
	pass