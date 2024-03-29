import keyboard, time, os, typing, threading, subprocess, sys
from datetime import datetime, timedelta
from handle_system import show_console, hide_console, time_since_input, wipe


print(" > vars")
f3d = "C:/Users/calvi/3D Objects"
interval = 120
hotkeys = {}
time_tracking = False
afk = False
app_running = False

print(" > functions")
def run(app: typing.Callable, console: bool, run_as_subprocess: bool = False):
    global app_running
    if app_running or run_as_subprocess:
        cmd = [sys.executable, '-c', f'from {app.__module__} import {app.__name__}; {app.__name__}()']
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        threading.Thread(target=run_app, args=(app, console), daemon=True).start()
        
def run_app(app: typing.Callable, console: bool = True):
    global app_running
    show_console() if console else None
    try:
        app_running = True
        app()
        app_running = False
        if os.name == 'nt':
            import winsound
            winsound.Beep(500, 200)
    except Exception as e:
        app_running = False
        print(e)
    hide(2) if console else None

def hide(seconds: int):
    print("\n")
    for i in range(seconds, 0, -1):
        print(f"  > closing in {i}", end='\r')
        time.sleep(1)
    hide_console()

def add_hotkey(hotkey: str, app: typing.Callable, console: bool = True, run_as_subprocess: bool = False):
    keyboard.add_hotkey(hotkey, lambda: run(app, console, run_as_subprocess))
    hotkeys[hotkey.split("+")[-1]] = str(app.__name__)

print(" > hotkeys")
def show_hotkeys():
    show_console()
    print("hotkeys\n")
    sorted_hotkeys = {k: hotkeys[k] for k in sorted(hotkeys)}
    for key in sorted_hotkeys:
        print("    ", key, sorted_hotkeys[key])
    hide(3)
add_hotkey('shift+ctrl+alt+k', show_hotkeys)

from handle_assistant import ffmpeg_assist
add_hotkey('shift+ctrl+alt+f', ffmpeg_assist)

from handle_clipboard import perform_ocr_on_clipboard, fix_windows_file_path_on_clipboard, type_clipboard_contents
add_hotkey('shift+ctrl+alt+l', perform_ocr_on_clipboard)
add_hotkey('shift+ctrl+alt+[', fix_windows_file_path_on_clipboard)
add_hotkey('shift+ctrl+alt+v', type_clipboard_contents, console=False)


from handle_time import punch, show_last_n_lines, timer
def afk_monitor():
    global afk
    ms = interval * 1000
    while True:
        if not afk:
            if time_since_input() > ms:
                show_console()
                print("\n")
                afk = True
                wait = 9
                for i in range(wait, 0, -1):
                    print(f"  > afk in {i}", end='\r')
                    if time_since_input() < ms:
                        afk = False
                        break
                    time.sleep(1)
                hide_console()
                if afk:
                    punch("o", "afk", datetime.now()-timedelta(seconds=interval+wait))
        else:
            pass
        time.sleep(interval)
def punch_and_start_afk_monitoring():
    global time_tracking, afk
    if not time_tracking:
        threading.Thread(target=afk_monitor, daemon=True).start()
        time_tracking = True
    afk = False
    punch()
add_hotkey('shift+ctrl+alt+a', punch_and_start_afk_monitoring)
add_hotkey('shift+ctrl+alt+w', show_last_n_lines)
add_hotkey('shift+ctrl+alt+q', timer, run_as_subprocess=True)

from handle_youtube import download_with_ui, download_transcript_with_ui
add_hotkey('shift+ctrl+alt+y', download_with_ui)
add_hotkey('shift+ctrl+alt+t', download_transcript_with_ui)

from handle_strings import godlike_copypaste, submit_to_sheets, notes_loop
from handle_twitter import tweet
add_hotkey('shift+ctrl+alt+b', godlike_copypaste)
add_hotkey('shift+ctrl+alt+s', tweet)
add_hotkey('shift+ctrl+alt+n', notes_loop, run_as_subprocess=True)

from ableton_demo_creater import wav_to_mp3
add_hotkey('shift+ctrl+alt+d', wav_to_mp3)

show_hotkeys()
keyboard.wait()
