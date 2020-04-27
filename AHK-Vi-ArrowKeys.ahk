; AHK-Vi-ArrowKeys
; Author: Parker Link
; License: MIT License
; Developed: Apr. 25, 2020 (thanks, COVID-19)

; Functionality: 
; Press and hold D. While D pressed, use the right hand home row to emulate arrow key presses (as per VI standard).

; Sources/References:
; https://autohotkey.com/board/topic/62491-pressing-two-keys-simultaneously-to-do-an-action/

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
	
	; ; D Press has started
	; +d::
	; d::
	; 	KeyWait d ; wait for d key to be released

	; 	;msgbox Start PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%

	; 	; Ensure that no VI keys were used
	; 	If (A_PriorKey != "h" && A_PriorKey != "j" && A_PriorKey != "k" && A_PriorKey != "l") ; user didn't type a VI key
	; 			&& (A_ThisHotkey = "d" || A_ThisHotkey = "+d") { ; verify user didn't type a VI key

	; 		If (A_PriorKey = "d") { ; user only typed a "d"
	; 			;msgbox Version A: PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%
	; 		 	if (A_ThisHotkey = "d") {
	; 		 		SendInput d
	; 		 	}
	; 		 	if (A_ThisHotkey = "+d") {
	; 		 		SendInput D
	; 		 	}
	; 		}
	; 		Else {
	; 			; User typed another key before releasing d...erase that key, make the d, then type the other key (effectively switch their order)
	; 			;msgbox Version B: PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%
				
	; 			if (A_ThisHotkey = "d") {
	; 		 		SendInput {BackSpace}d{%A_PriorKey%}
	; 		 	}
	; 		 	if (A_ThisHotkey = "+d") {
	; 		 		SendInput {BackSpace}D{%A_PriorKey%}
	; 		 	}

	; 		}

	; 	}
	; 	Return

	+d::
	d::
<<<<<<< HEAD
		; Starts running as soon as d is pressed down
		;MakeTooltip("d hotkey occured inside #IfDPressed")
		;KeyWait d ; wait for d to be released
		Input, InputTextVar, L1 T0.3 I0

		if (ErrorLevel = "Timeout") {
			ErrorLevel = 0 ; reset the error level for next time
			MakeTooltip("Timeout occured, no fast character received, wait for normal release.")
			KeyWait d
			if ((A_ThisHotkey = "d" or A_ThisHotkey = "+d") and A_PriorKey != "Backspace") { ;  no vi key was pressed, and the user didn't try to delete the 'd'
				SendInput %A_ThisHotkey% ; send either uppercase or lowercase d
			}
			;Else
			;	MakeTooltip("Char was a vi key or backspace." isCharacterVIKey(A_ThisHotkey))
		}
		else {
			; Key received in the fast input, send that key after a d
			MakeTooltip("No timeout, using fast received character.")

			if (A_PriorKey = "d") {
				SendInput %A_ThisHotkey%%A_ThisHotkey%%InputTextVar%  ; two d/D's were typed very fast back to back
			}
			Else {
				SendInput %A_ThisHotkey%%InputTextVar% ; send d/D then the fast received character
			}
		}

		MakeTooltip("Presses -> PriorHotkey:  " A_PriorHotkey ", ThisHotkey: " A_ThisHotkey " , PriorKey: " A_PriorKey ", Input: " InputTextVar)
=======
		KeyWait d ; wait for d to be released
		if (A_ThisHotkey = "d" || A_ThisHotkey = "+d") {
			SendInput %A_ThisHotkey% ; send either uppercase or lowercase d
		}
>>>>>>> parent of 9998c14... Setup system using Input function to read extremely fast input
		Return



	; Remap the VI Keys
	h::Left
	j::Down
	k::Up
	l::Right

	; Remap Normal Keys
	+a::
	a::
	b::
	+b::
	c::
	+c::
	e::
	+e::
	f::
	+f::
	g::
	+g::
	i::
	+i::
	m::
	+m::
	n::
	+n::
	o::
	+o::
	p::
	+p::
	q::
	+q::
	r::
	+r::
	s::
	+s::
	t::
	+t::
	u::
	+u::
	v::
	+v::
	w::
	+w::
	x::
	+x::
	y::
	+y::
	z::
	+z::
	'::
	+'::
	"::
	Space::
	+Space::
		;msgbox Version A: PriorHotkey:  %A_PriorHotkey% , ThisHotkey: %A_ThisHotkey% , PriorKey: %A_PriorKey%
		If (A_ThisHotkey = "Space" or A_ThisHotkey = "+Space") {
			SendInput %A_PriorHotkey%{Space} ; Send d/D, then send the space character typed
		}
		Else {
			SendInput %A_PriorHotkey%%A_ThisHotkey% ; Send d/D, then send the uppercase/lowercase character typed
		}
		Return

#If ; close

; Assign a Hotkey to Quit the Script (for development purposes)
End::
	MsgBox Quitting Script
	ExitApp