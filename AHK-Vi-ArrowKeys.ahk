; AHK-Vi-ArrowKeys
; Author: Parker Link
; License: MIT License
; Developed: Apr. 25, 2020 (thanks, COVID-19)

; Functionality: 
; Press S+D at the same time (or within the threshold set below).
; While S+D pressed, use the right hand home row to emulate arrow key presses (as per VI standard)

; Sources/References:
; https://autohotkey.com/board/topic/62491-pressing-two-keys-simultaneously-to-do-an-action/

; Set the Threshold for S+D to be considered "simultaneous" (setting this too high makes words like "words") glitch when typed too fast
timeThreshold = 500


; s::
; d::

; If (A_PriorHotkey="s" || A_PriorHotkey="d") && A_TimeSincePriorHotkey<500 && A_PriorHotkey<>A_ThisHotKey
	
; 	MsgBox You pressed "s+d"

; Return

;; Triggers when either s or d is pressed
; s::
; d::

;SoundBeep

; If only one of the trigger keys is pressed
#If !(GetKeyState("s", "P") && GetKeyState("d", "P"))
	; s::
	; 	Sleep, %timeThreshold%
	; 	If !GetKeyState("d", "P")
	; 		Send s
	; 	Return

; d::
; 	Sleep, %timeThreshold%
; 	If !GetKeyState("s", "P")
; 		Send d
; Return

#If ; close



#If GetKeyState("d", "P") ; && GetKeyState("s", "P")
	; Don't type these keys when both of them are pressed (simple)
	; s::
	; 	Sleep, %timeThreshold%
	; 	If !GetKeyState("d", "P")
	; 		Send s
	

	; $d:: ; dollar sign means it can't be triggered by itself
	; 	SoundBeep
	; 	If A_PriorHotkey = "d"
	; 		; Another key was pressed
	; 		Send d
	; 	Return

	d::
		KeyWait d ; wait for d key to be released
		; msgbox Prior:  %A_PriorHotkey% , This: %A_ThisHotkey%
		If (A_ThisHotkey = "d")
			Send d
		Return

	h::Left
	j::Down
	k::Up
	l::Right

#If ; close


; Assign a Hotkey to Quit the Script (for development purposes)
End::
	MsgBox Quitting Script
	ExitApp