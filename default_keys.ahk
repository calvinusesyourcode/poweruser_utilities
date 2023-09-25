#Requires AutoHotkey v2.0
#Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir A_WorkingDir  ; Ensures a consistent starting directory.
#SingleInstance

DetectHiddenWindows 1
SetTitleMatchMode 2
SetNumLockState "AlwaysOn"


numpad := False
pedalboard := False
abletonKeys := False

my3dFolder := "C:/Users/calvi/3D Objects"

+^!k::{
Run "C:\Users\calvi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\PanoramaStudio 3 Pro.lnk"
}

+^!h::{
Run my3dFolder . "\poweruser_utilities\ableton_demo_creater.py"
}



+^!y::{
Run my3dFolder . "whisper_tool/download_with_ui.py"
}
+^!u::{
Run my3dFolder . "whisper_tool/trim_audio_with_ui.py"
}
+^!t::{
Run my3dFolder . "whisper_tool/to_mp3_with_ui.py"
}
+^!i::{
Run my3dFolder . "whisper_tool/to_audio_with_ui.py"
}

+^!n::{
url := my3dFolder . "\repo_opener.py - Shortcut.lnk"
Run url
}

+^!b::{
Run my3dFolder . "\godlike_copypaste.py - Shortcut.lnk"
}

+^!o::{
Run my3dFolder . "\crypto_bot\test\main.js"
}


CapsLock::{
Send "{Esc}"
}

interface_script := FileRead(A_WorkingDir . "\scripturl.txt")
Tooltip interface_script
Sleep 100
Tooltip
interface_json := "?sheetid=%221cOyI1cq8rm85hJk0SuNahlMUaLps5N5Z4DHW3q1tzWQ%22"

Tab::{
Send "    "
}

Hotkey "Tab", "Off"

+^!a::{
Hotkey "Tab", "On"
userText := InputBox(" " , "CUSTOM ENTRY","W400 H80",).value
app_map := Map(
	"t" , "thoughts",
	"p" , "punchcard",
	"a" , "activity",
	"j" , "journal",
	"2" , "todo",
	"to", "todo",
	"v", "videos")
if userText {
	try {
		app := SubStr(userText,1,InStr(userText,"    ")-1)
		userText := SubStr(userText,InStr(userText,"    ")+4)
		if app_map.Has(app)
		app := app_map[app]
	} catch {
		app := "test"
	}
url := interface_script . interface_json . "&app=%22" . app . "_ahk%22&info=%22" . A_Now . customEncode(1,userText) . "%22"
;
text := AppsScriptRequest(url,true)
;
if !(InStr(text, "done")) {
ToolTip text
Sleep 10000
ToolTip 
}
}
Hotkey "Tab", "Off"
}

+^!q::{
if WinActive("Ableton Live 11") {
	app := "todo"
	subject := "ableton"
} else if WinActive("Premiere Pro 2020") {
	app := "todo"
	subject := "premiere"
} else if WinActive("GNU Image") {
	app := "todo"
	subject := "gimp"
} else {
	Hotkey "Tab", "On"
	userText := InputBox(" " , "_get","W400 H80",).value
	subject_map := Map(
		"abl" , "ableton",
		"a" , "ableton",
		"p" , "premiere",
		"pr" , "premiere",
		"w", "website",
		"web", "website")
	if userText {
		if InStr(userText,":") {
			try {
				app := SubStr(userText,2,InStr(userText,"    ")-2)
				subject := SubStr(userText,InStr(userText,"    ")+4)
			} catch {
				app := SubStr(userText,2)
				subject := ""
				userText := ""
			}
		} else {
			app := "todo"
			try {
				subject := subject_map[userText]
			} catch {
				subject := userText
			}
		}
	} else {
	return
	}
Hotkey "Tab", "Off"
}
if app {
url := interface_script . interface_json . "&app=%22" . app . "_get%22&info=%22" . customEncode(1,subject) . "%22"
text := AppsScriptRequest(url,false)
;
try {
FileDelete(A_WorkingDir . "\return_string.txt")
Sleep 10
}
if (InStr(text, "no data retrieved from sheet")) {
	Tooltip text
	Sleep 5000
	Tooltip
} else {
FileAppend StrReplace(text, "\n", "`r"), A_WorkingDir . "\return_string.txt"
Run A_WorkingDir . "\return_string.txt"
}
}
}

+^!e::{
userText := InputBox("enter the item number" , "_complete","W400 H120",).value

text := FileRead(A_WorkingDir . "\return_string.txt")
first_line := SubStr(text,1,InStr(text,"`n"))

if(InStr(first_line,";")){
	app := SubStr(first_line,1,InStr(text,";")-1)
	subject := SubStr(first_line,InStr(text,";")+1,InStr(text,"`n")-InStr(text,";")-1)
} else {
	app := SubStr(first_line,1,InStr(text,"`n")-1)
	subject := "none"
}

item_onward := SubStr(text,InStr(text,"     " . userText . " — ")+9)
item := SubStr(item_onward,StrLen(userText),InStr(item_onward,"`n")-StrLen(userText))

url := interface_script . interface_json . "&app=%22" . app . "_complete%22&info=%22" . customEncode(1,subject) . "%22&item_num=%22" . userText . "%22"
text := AppsScriptRequest(url,false)

if !(InStr(text, "done")) {
ToolTip text
Sleep 10000
ToolTip 
}
}



;--------------------------------------------------------------------------------------------------------------------
;		FUNCTIONS
;--------------------------------------------------------------------------------------------------------------------

ConnectedToInternet(flag:="0x40") { 
	Return DllCall("Wininet.dll\InternetGetConnectedState", "Str", flag ,"Int",0) 
}

customEncode(mode, text) {
      specialChars := "_ !@#$%^&*()-+={[}]:`;\" . '"' . "'>.<,?/|~``"
      encodedChars := [
        "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08",
        "H09", "H0A", "H0B", "H0C", "H0D", "H0E", "H0F", "H0G",
        "H0H", "H0I", "H0J", "H0K", "H0L", "H0M", "H0N", "H0O",
        "H0P", "H0Q", "H0R", "H0S", "H0T", "H0U", "H0V", "H0W",
        "H0X", "H0Y", "H0Z", "H10", "H11", "H12", "H13", "H14",
        "H15", "H16", "H17", "H18", "H19", "H1A", "H1B", "H1C",
        "H1D", "H1E", "H1F", "H1G", "H1H", "H1I", "H1J", "H1K",
        "H1L", "H1M", "H1N", "H1O", "H1P", "H1Q", "H1R", "H1S"
      ]


if (mode == 1) {
        encodedText := ""
        Loop StrLen(text) {
            char := SubStr(text, A_Index, 1)
            index1 := InStr(specialChars, char)
            if (char = " " && SubStr(text, A_Index + 1, 1) = " " && SubStr(text, A_Index + 2, 1) = " " && SubStr(text, A_Index + 3, 1) = " ") {
		encodedText .= "_H1S"
		A_Index += 3
		} else if (index1 > 0) {
                	encodedText .= "_" . encodedChars[index1]
		} else {
                	encodedText .= char
		}	
        }
        return encodedText
    } else if (mode == 0) {
        MsgBox "Sorry, I have not built decoding functionality yet"
    } else {
        throw "Invalid mode. Use 1 for encoding and 0 for decoding."
    }
}

AppsScriptRequest(theURL,save_offline) {
try {
	A_Clipboard := theURL
	whr := ComObject("WinHttp.WinHttpRequest.5.1")
	whr.Open("GET", theURL, true)
	whr.Send()
	; Using 'true' above and the call below allows the script to remain responsive.
	whr.WaitForResponse()
	return whr.ResponseText
} catch {
	if save_offline {
		text := "`r" . theURL
		FileAppend text, A_WorkingDir . "\offline-bunker.txt"
		Tooltip "saved offline"
		Sleep 1000
		Tooltip
	}
}
}


;--------------------------------------------------------------------------------------------------------------------
;		SUBMIT offline-bunker.txt
;--------------------------------------------------------------------------------------------------------------------

try { 												; check connection and upload
	testURL := "https://script.google.com/macros/s/AKfycbwnX_LKtIskpp208iqoqyYYUNWQiol38UYd0PhRaA4-kYCtxoavJq--QsUozldZTaRs/exec?sheetid=%221cOyI1cq8rm85hJk0SuNahlMUaLps5N5Z4DHW3q1tzWQ%22&app=%22testconnection%22"
	whr0 := ComObject("WinHttp.WinHttpRequest.5.1")
	whr0.Open("GET", testURL, true)
	whr0.Send()
	; Using 'true' above and the call below allows the script to remain responsive.
	whr0.WaitForResponse()
	text0 := whr0.ResponseText
	
	if (text0 ~= "i)\A(connection to mind interface stable)\z") {
		string1 := FileRead(A_WorkingDir . "\offline-bunker.txt")
		
		if string1 {
			Tooltip "UPLOADING offline-bunker.txt"
			array1 := StrSplit(string1, "`r")

			counter := 0
			for index, value in array1 {
				if value { 							
					text0 := AppsScriptRequest(value,false)
					counter += 1
				}
			}
		
			Tooltip
			FileDelete(A_WorkingDir . "\offline-bunker.txt")
			Tooltip "submitted " . counter . " data point(s)."
			Sleep 2000
			Tooltip
		}
	}
}



;--------------------------------------------------------------------------------------------------------------------
;		Keybinds
;--------------------------------------------------------------------------------------------------------------------



^+!1::{
url := "https://www.google.com/search?q=" . StrReplace(InputBox(, "google","W200 H80",).value, " ","+")
Run url
}

^+!2::{
url := "https://chat.openai.com/chat"
Run url
}

^+!3::{
url := "https://docs.google.com/spreadsheets/d/1cOyI1cq8rm85hJk0SuNahlMUaLps5N5Z4DHW3q1tzWQ/edit#gid=857549180"
Run url
}

^+!4::{
url := "https://script.google.com/home/projects/1crSbgtyUyZr7WMDoE1gBA2t7JvKGodroRsVG4m7klfTyIOmtF1d-QOZq/edit"
Run url
}

^+!5::{
url := "https://www.autohotkey.com/docs/v2/"
Run url
}

^+!r::{
url := A_Clipboard
url := StrReplace(url,"\\","\")
Run url
}

+^!x::{
url := A_WorkingDir . "\default-keys.ahk"
Run url
}

+^!z::{
Edit
}

+^!-::{
SendText "—"
}

+^!=::{
SendText "calvinducharme@gmail.com"
}

^+!d::{
Run "C:\Users\calvi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\open_ssd1cad.lnk"
}

^+!m::{
Run "C:\Shortcuts\Test Box.lnk"
}

+^!p::{
SendText A_Clipboard
}

+^!v::{

clip := customEncode(1,A_Clipboard)
scripturl := interface_script . interface_json . "&app=%22misc_pasteUrl%22&url=%22"
url := scripturl . clip . "%22"

A_Clipboard := url
text := AppsScriptRequest(url,true)

ToolTip text
Sleep 1000
ToolTip
}

+^!c::{
url := "https://script.google.com/macros/s/AKfycbxvu1pKEZGAqZhx-oJWvCoICzSRONw3Y7VCuGP_ZwtN3FbQNUtNzSQ7A16tVjsFTcso/exec?app=%22misc_copyUrl%22"
A_Clipboard := AppsScriptRequest(url,true)
ToolTip A_Clipboard
Sleep 1000
ToolTip
}

