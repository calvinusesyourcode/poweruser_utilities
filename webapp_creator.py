from ahk import AHK
import os, re, time, subprocess

ahk = AHK()

os.chdir('C:\\Users\\calvi\\3D Objects')
app_name = "webapp"+str(len([x for x in os.listdir() if re.search('webapp', x)]))
print(app_name)


def send_these(commands):
        for cmd in commands:
                print(cmd)
                if "time.sleep" in cmd:
                        time.sleep(float(cmd.split("time.sleep(")[1].split(")")[0]))
                elif "check_if_done" in cmd:
                        while True:
                                # type a random word from a list of words and then select it and copy it and check if it is in the clipboard
                                ahk.set_clipboard("")
                                ahk.send_input("hello")
                                ahk.send_input("{Left}")
                                time.sleep(0.1)
                                ahk.send_input("{Shift down}")
                                time.sleep(0.1)
                                ahk.send_input("{Left}{Left}{Left}{Left}{Left}")
                                time.sleep(0.1)
                                ahk.send_input("{Shift up}")
                                time.sleep(0.1)
                                ahk.send_input("^c")
                                time.sleep(0.1)
                                ahk.send_input("{Right}{Right}")
                                for i in range(20):
                                        ahk.send_input("{Backspace}")
                                print(len(str(ahk.get_clipboard())))
                                if str(ahk.get_clipboard()) == "hello":
                                        print("Process completed")
                                        ahk.set_clipboard("")
                                        break
                                time.sleep(2)
                else:
                        if cmd[0] == "$":
                                ahk.send_input(cmd[1:])
                                time.sleep(0.05)
                                ahk.send_input("{Enter}")
                                time.sleep(0.3)
                        elif cmd[0] == "%":
                                ahk.send_input(cmd[1:])
                                time.sleep(0.05)
                                ahk.send_input("{Enter}")
                                send_these(["check_if_done"])
                        elif cmd[0] == "!":
                                ahk.send_input(cmd)
                                time.sleep(1)
                        else:
                                ahk.send_input(cmd)
                                time.sleep(0.3)


# run cmd with ahk
ahk.set_title_match_mode(2)
ahk.run_script('Run "C:\\Users\\calvi\\3D Objects\\cmd.exe - Shortcut.lnk"')
ahk.win_wait("cmd.exe")
ahk.win_activate("cmd.exe")
send_these([
        "cd C:\\Users\\calvi\\3D Objects",
        "{Enter}",
        f'npx create-next-app "{app_name}"',
        "{Enter}",
])
time.sleep(4)
send_these([
        "{Enter}",
        "{Right}",
        "{Enter}",
        "{Enter}",
        "{Enter}",
        "{Enter}",
        "{Enter}",
        "check_if_done",
        '$cd "'+app_name+'"',
        '%npm install firebase react-firebase-hooks',
        "$firebase init",
        "time.sleep(3)",
        "$y",
        "{Down}",
        "{Space}",
        "{Down}",
        "{Space}",
        "{Down}",
        "{Down}",
        "{Down}",
        "{Space}",
        "{Down}",
        "{Down}",
        "{Space}",
        "{Down}",
        "{Space}",
        "{Enter}",
        "${Down}",
        f"$calvin-{app_name}",
        "{Enter}",
        "time.sleep(50)"

])
os.chdir(f"C:\\Users\\calvi\\3D Objects\\{app_name}")
print("done")
# fetch file pages/index.js and change <title> to app_name
with open(f"C:\\Users\\calvi\\3D Objects\\{app_name}\\pages\\index.js", 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        output = []
        for line in lines:
                if re.search('<title>', line):
                        line = "<title>"+app_name+"</title>"
                output.append(line)
        f.writelines(output)
time.sleep(1000)
