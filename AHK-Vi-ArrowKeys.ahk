; AHK-Vi-ArrowKeys
; Author: Parker Link
; License: MIT License
; Developed: Apr. 25, 2020 (thanks, COVID-19)

; Functionality: 
; Press and hold D. While D pressed, use the right hand home row to emulate arrow key presses (as per VI standard).

; Sources/References:
; https://autohotkey.com/board/topic/62491-pressing-two-keys-simultaneously-to-do-an-action/

dJustPressed = 0

; Fixes words like "world" and "workd" where a VI key is followed by a 'd'
#If (GetKeyState("h", "P") or GetKeyState("j", "P") or GetKeyState("k", "P") or GetKeyState("l", "P"))
	; If any of the VI keys are down
	d::
		Send d
		Return
	+d::
		Send D
		Return
#If ; close


#If GetKeyState("d", "P")
	
	+d::
	d::
		dJustPressed = 1
		MakeTooltip("dJustPressed set to true", 1000)
		;KeyWait d ; wait for d to be released
		while (GetKeyState("d", "P") and A_PriorKey = "d") {
		; 	MakeTooltip("In while loop", 250)
		}

		if (A_ThisHotkey = "d" || A_ThisHotkey = "+d") {
			SendInput %A_ThisHotkey% ; send either uppercase or lowercase d
		}
		Return



	; Remap the VI Keys
	h::
		if (dJustPressed == 1) {
			SendInput {Backspace}
			dJustPressed = 0
		}
		SendInput {Left}
		Return

	j::
		if (dJustPressed == 1) {
			SendInput {Backspace}
			dJustPressed = 0
		}
		SendInput {Down}
		Return

	k::
		if (dJustPressed == 1) {
			SendInput {Backspace}
			dJustPressed = 0
		}
		SendInput {Up}
		Return
	l::
		if (dJustPressed == 1) {
			SendInput {Backspace}
			dJustPressed = 0
		}
		SendInput {Right}
		Return


#If ; close

; Assign a Hotkey to Quit the Script (for development purposes)
End::
	MsgBox Quitting Script
	ExitApp

RemoveToolTip:
	ToolTip
	Return

MakeTooltip(message, time:=2500) {
	if 1 { ; change to 0 to disable tooltips
		ToolTip, %message%, 0, 0
		SetTimer, RemoveToolTip, %time%
	}
}

isCharacterVIKey(char) {
	return (char = "h" and char = "j" and char = "k" and char = "l") ; single equals is case insensitive
}