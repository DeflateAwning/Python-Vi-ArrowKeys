# Python-Vi-ArrowKeys
A Python script that works like Karabiner for Mac's VI mode (but for Windows, now). Press and hold "D", and use the right hand home row to emulate arrow keys, based on the VI mapping.

This software creates a System Tray icon, and can be enabled/disabled from that icon. **Number lock must be off** for the keypad to work/selection to work properly (see Known Issues).

This project was originally attempted in AHK (see the `ahk-attempt` branch), but switched to Python for more flexibility. While it should be cross-platform, it has only been tested on Windows.

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

## Acknowledgments
* [Toshi T.](https://github.com/robotoshi) for assistance in debugging "Discord" bug, and helping to explore the Number Lock issues.
* [Keyboard icon](https://icons8.com/icons/set/keyboard) by [Icons8](https://icons8.com).

## Known Issues/Limitations
### Issues (Fine for Now)
* Not all **key up events are triggered** properly for normal characters (ex: 'world'). This is speculative, but probably not actually an issue.
* 'D' presses now occur when 'd' is lifted (feels delayed). For video games (especially those that use WASD-keys), you'll likely want to disable this software, or use Raw Input grabbing in the video game.
* Some non-alphanumeric keys, when typed very fast before or after a 'd', may behave weirdly: their position may be switched with the 'd' typed. Examples of this include the 'tab' character. This can be solved on a character-by-character basis by adding them to the `config["hookKeys"]` list.
* This program works with Synergy (keyboard/mouse sharing software) on the host computer, as long as Synergy is run in non-elevated mode. If Synergy is disabled then re-enabled, this program must be Restarted with the "Restart" button in the tray.
* **System Compatibility:** This software does not run on Mac with systray. No other testing/development has been done.
* This software didn't work with preliminary testing with Dvorak. Further development efforts may be required to add alternative keyboard layout options.

### Problematic Issues
* Serious bug with keyboard having a number pad. When NUMLOCK is TURNED ON, the shift key does not work for arrow key presses.
	* Example: Selection using the VI key mapping doesn't work while NUMLOCK ON
	* This is currently fixed by requiring NUMLOCK to be TURNED OFF, and all keypad keys act as their number always.

If you come up with a fix, please make a pull request.
If you notice a bug, please open an issue and/or make a pull request.

## Future Ideas:
* Consider the following mapping(s):
	* 0 -> go to start of line (ctrl+up?)
	* Investigate other potential bindings.
* Add a "disable for x amount of time" submenu in system tray icon.
* Add an "Features Enabled" submenu in the system tray icon to enable/disable specific features (example: disable the d+b and d+w bindings for people typing "db" frequently).

## Refactoring Suggestions
* Combine `gstate["viTriggeredYet"]` and `gstate["dSentYet"]` into a single `gstate["stillSendD"]` variable, that records whether or not to send the 'd'. Resets (to True) on the start of a d press, and gets flagged (to False) when a VI key is pressed, or the first time a 'd' is sent.
