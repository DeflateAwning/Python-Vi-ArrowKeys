# AHK-Vi-ArrowKeys
An AutoHotkey script that works like Karabiner for Mac's VI mode (but for Windows, now). Press and hold "D", and use the right hand home row to emulate arrow keys, based on the VI mapping.

In a previous version of Karabiner for Mac, this mode was triggered by pressing S+D. However, now it is triggered by only pressing D (as per the most recent version of the Mac software).

## List of Remappings
While holding D:
* H -> Left Arrow
* J -> Down Arrow
* K -> Up Arrow
* L -> Right Arrow

If you don't press any of those before releasing the D key, a "d" is typed.

Modifier keys (specifically, shift) are applied as pressed. This tool can be used to move around, or select text.

## Known Issues
* Characters following a letter 'd' may be swapped from how you intended them. Example, type the word "did" a bunch of times with spaces between them.
	* This is partially fixed in the `Else` block right before the VI key remapping. However, this fix doesn't really work that well.

If you come up with a fix, please make a pull request.