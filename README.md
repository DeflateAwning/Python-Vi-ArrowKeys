# Python-Vi-ArrowKeys
A Python script that works like Karabiner for Mac's VI mode (but for Windows, now). Press and hold "D", and use the right hand home row to emulate arrow keys, based on the VI mapping.

This software creates a System Tray icon, and can be enabled/disabled from that icon. **Number lock must be off** for the keypad to work/selection to work properly (see Known Issues).

This project was originally attempted in AHK (see the `ahk-attempt` branch), but switched to Python for more flexibility. While it should be cross-platform, it has only beed tested on Windows.

In a previous version of Karabiner for Mac, this mode was triggered by pressing S+D. However, now it is triggered by only pressing D (as per the most recent version of the Mac software).

## List of Remappings
While holding D:
* H -> Left Arrow
* J -> Down Arrow
* K -> Up Arrow
* L -> Right Arrow
* W -> jump forward a word
* B -> jump backwards a word

If you don't press any of those before releasing the D key, a "d" is typed (like normal).

Modifier keys (specifically, shift) are applied as pressed. This tool can be used to move around, or select text.

## Acknowledgements
* [Toshiro T.](https://github.com/robotoshi) for assistance in debugging "Discord" bug, and helping to explore the Number Lock issues.
* [Keyboard icon](https://icons8.com/icons/set/keyboard) by [Icons8](https://icons8.com).

## Known Issues/Limitations
### Inherent Limitations (Not Required)
* Not all **key up events are triggered** properly for normal characters (ex: 'world'). This is speculative, but probably not actually an issue.
* 'D' presses now occur when 'd' is lifted (feels delayed). For video games (especially those that use WASD-keys), you'll likely want to disable this software, or use Raw Input grabbing in the video game.
* Some keys, when typed very fast before or after a 'd', may behaviour weirdly: their position may be switched with the 'd' key. Examples of this include the 'tab' character. This can be solved on a character-by-character basis by adding them to the `config["hookKeys"]` list.
* This program works with Synergy (keyboard/mouse sharing software) on the host computer, as long as Synergy is run in non-elevated mode. If Synergy is disabled then re-enabled, it must be Restarted with the "Restart" button in the tray.
* **System Compatibility:** This software does not run on Mac with systray. No other testing/development has been done.

### Problematic Issues
* Serious bug with keyboard having a number pad. When NUMLOCK is TURNED ON, the shift key does not work for arrow key presses.
	* Example: Selection using the VI key mapping doesn't work while NUMLOCK ON
	* This is currently fixed by requring NUMLOCK to be TURNED OFF, and all keypad keys act as their number.

If you come up with a fix, please make a pull request.
If you notice a bug, please open an issue and/or make a pull request.

## Future Ideas:
* Consider the following mapping(s):
	* 0 -> go to start of line (ctrl+up?)
* Add a "disable for x amount of time" submenu in system tray icon.
* Add an "Features Enabled" submenu in the system tray icon.

There are even more VI mappings that can be added after. We'll start with these, though.

## Refactoring Suggestions
* Combine `gstate["viTriggeredYet"]` and `gstate["dSentYet"]` into a single `gstate["stillSendD"]` variable, that records whether or not to send the 'd'. Resets (to True) on the start of a d press, and gets flagged (to False) when a VI key is pressed, or the first time a 'd' is sent.

## Code Structure
The following sections are labelled with comments in the Python code. Each section is within the `hookCallback(event)` function, and handles a certain type of key press/release occurrence.

### **Section 1:** Fast exit hotkey
By pressing the "END" key, the program is exited. Can be disabled in the `config['enableQuickExit']`. Useful for stopping the program if any bugs occur and the keyboard is blocked.

### **Section 2:** Record keys currently down
Updates the set() at `gstate['down']` with lowercase names of all keys currently pressed. Also updates the capslock state.

### **Section 3:** Pass Through Normal Keys
Passes through normal (non-VI) keys. This section is activated when 'd' is not held down, or when the key being received is not a VI key.

* If the key event_type is UP (key received is being released), a release is simply sent to the computer.
* If the key event_type is DOWN (key received is being pressed):
	1. We check to see if 'd' is pressed down currently, and see if it has been sent for this time it is pressed.
		* If this is the case, as would be when **typing "cards" very quickly,** (known as the 'cards' bug) send a 'd' before the received event
	2. Finally, send the received event

### **Section 4:** Pass Through 'd' on UP Event
Normally (neglecting fast consecutive presses), the 'd' key is sent on a key up event. However, it is not sent if either 1) a VI key was pressed since it was pressed down, or 2) it was already sent because of a fast consecutive press

### **Section 5:** Send 'd' after VI key (fixes 'world' bug)
* When you type the word "world" fast, the 'l' and 'd' cause a unique case that must be caught here.
* The `if any([...]) and <d pressed down right now>` statement checks to see if any VI keys are currently pressed, and checks to see if the current event is 'd DOWN'.

### **Section 6:** Perform VI Remapping
If the key is a mappable key, and 'd' is currently held down, send the appropriate arrowkey.

### **Section 7**: Print Debug Info
Prints debug info about the current event, and various states. In the future (or as needed), add a printout of `gstate` to the end.

Sample of Debug Info: `New Event: type(down)   name(42 = shift)                keysDown(space|shift))`

