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

;#MaxThreads 1

#If GetKeyState("d", "P")
	
	; D Press has started
	+d::
	d::
		KeyWait d ; wait for d key to be released

		;msgbox Start PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%

		; Ensure that no VI keys were used
		If (A_PriorKey != "h" && A_PriorKey != "j" && A_PriorKey != "k" && A_PriorKey != "l") ; user didn't type a VI key
				&& (A_ThisHotkey = "d" || A_ThisHotkey = "+d") { ; verify user didn't type a VI key

			If (A_PriorKey = "d") { ; user only typed a "d"
				;msgbox Version A: PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%
			 	if (A_ThisHotkey = "d") {
			 		SendInput d
			 	}
			 	if (A_ThisHotkey = "+d") {
			 		SendInput D
			 	}
			}
			Else {
				; User typed another key before releasing d...erase that key, make the d, then type the other key (effectively switch their order)
				;msgbox Version B: PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%
				
				if (A_ThisHotkey = "d") {
			 		SendInput {BackSpace}d{%A_PriorKey%}
			 	}
			 	if (A_ThisHotkey = "+d") {
			 		SendInput {BackSpace}D{%A_PriorKey%}
			 	}

			}

		}
		Return


	; Remap the VI Keys
	h::Left
	j::Down
	k::Up
	l::Right

#If ; close

; Assign a Hotkey to Quit the Script (for development purposes)
End::
	MsgBox Quitting Script
	ExitApp