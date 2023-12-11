# Read and parse the JSON file
$jsonFilePath = "C:\\Users\\calvi\\3D Objects\\poweruser_utilities\\powershell_test.json"
$jsonData = Get-Content -Path $jsonFilePath | ConvertFrom-Json

$targetPath = $jsonData.TargetPath
$hotkey = $jsonData.Hotkey
# $description = $jsonData.Description
# $iconLocation = $jsonData.IconLocation
$shortcutName = [System.IO.Path]::GetFileNameWithoutExtension($jsonData.TargetPath) + "_shortcut.lnk"

# Create VBScript code
$vbScript = @"
set WshShell = WScript.CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
set oShellLink = WshShell.CreateShortcut(strDesktop & "\\$shortcutName")
oShellLink.TargetPath = "$targetPath"
oShellLink.WindowStyle = 1
oShellLink.Hotkey = "$hotkey"
oShellLink.Save
"@
# oShellLink.IconLocation = "$iconLocation"
# oShellLink.Description = "$description"
# oShellLink.WorkingDirectory = strDesktop



# Create temporary VBScript file and run it
$tempVbsPath = "temp.vbs"
Set-Content -Path $tempVbsPath -Value $vbScript
cscript.exe $tempVbsPath
Remove-Item $tempVbsPath
