#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

keyList := []
keyList.insert(["d",950,0])   ; used this one to mark the shift left key
keyList.insert(["x",2850,0])
keyList.insert(["c",17100,0])
keyList.insert(["z",4590,0])  ;object = key,interval,nextInterval=0
keyList.insert(["v",900,0])

toggle := false
return

#IfWinActive, Diablo III
f1::
toggle := !toggle
if (toggle) {
	loop % keyList.MaxIndex()
		keyList[a_index][3] := a_tickcount + keyList[a_index][2] ;reset nextinterval to default interval
	settimer,auto,10
} else {
	settimer,auto,off
}
return

#IfWinActive, Diablo III
WheelUp::
 MouseClick Left
return

#IfWinActive, Diablo III
WheelDown::
 MouseClick Right
return


auto:
loop % keyList.MaxIndex() { ;loop through our array of keys
	if (a_tickcount > keyList[a_index][3]) { ;if enough time has passed since last press do something
		keyList[a_index][3] := a_tickcount + keyList[a_index][2] ;set next interval
		key := keyList[a_index][1]
		if (key != "d"){
			send {%key% down}
			sleep 50
			send {%key% up}
		}
		else{
			Send {Shift down}{LButton down}
			sleep 50
			Send {Shift up}{LButton up}
		}
	}
}
return
