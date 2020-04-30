# AHK-Vi-ArrowKeys
An ~AutoHotkey~ Python script that works like Karabiner for Mac's VI mode (but for Windows, now). Press and hold "D", and use the right hand home row to emulate arrow keys, based on the VI mapping.

This project was originally attempted in AHK, but switched to Python for more flexibility.

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
* Not all key up events are trigger properly for normal characters (ex: 'world'). This is speculative, but probably not actually an issue.
* "carsd/cards" bug
* "worl/world" bug

If you come up with a fix, please make a pull request.