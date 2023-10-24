import keyboard, time, os, typing, threading
from datetime import datetime, timedelta
from handle_system import show_console, hide_console, time_since_input, wipe

hide_console()

# variables
f3d = "C:/Users/calvi/3D Objects"
interval = 120
hotkeys = {}
time_tracking = False
afk = False

# functions
def run(app: typing.Callable):
    show_console()
    app()
    hide(3)

def hide(seconds: int):
    print("\n")
    for i in range(seconds, 0, -1):
        print(f"  > closing in {i}", end='\r')
        time.sleep(1)
    hide_console()

def add_hotkey(hotkey: str, app: typing.Callable):
    keyboard.add_hotkey(hotkey, lambda: run(app))
    hotkeys[hotkey.split("+")[-1]] = str(app.__name__)

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

def show_hotkeys():
    show_console()
    print("hotkeys\n")
    sorted_hotkeys = {k: hotkeys[k] for k in sorted(hotkeys)}
    for key in sorted_hotkeys:
        print("    ", key, sorted_hotkeys[key])
    hide(3)

def punch_and_start_afk_monitoring():
    global time_tracking, afk
    if not time_tracking:
        threading.Thread(target=afk_monitor, daemon=True).start()
        time_tracking = True
    afk = False
    punch()

# add hotkeys
add_hotkey('shift+ctrl+alt+k', show_hotkeys)

from handle_time import punch, show_last_n_lines
add_hotkey('shift+ctrl+alt+a', punch_and_start_afk_monitoring)
add_hotkey('shift+ctrl+alt+w', show_last_n_lines)


from handle_youtube import download_with_ui
add_hotkey('shift+ctrl+alt+y', download_with_ui)

from handle_strings import godlike_copypaste, submit_to_sheets
from handle_twitter import tweet
add_hotkey('shift+ctrl+alt+b', godlike_copypaste)
add_hotkey('shift+ctrl+alt+s', tweet)




# from handle_audio import to_mp3_with_ui, audio_to_audio_with_ui, trim_audio_with_ui
# keyboard.add_hotkey('shift+ctrl+alt+t', lambda: run())
# keyboard.add_hotkey('shift+ctrl+alt+u', lambda: run())
# keyboard.add_hotkey('shift+ctrl+alt+i', lambda: run())

from ableton_demo_creater import wav_to_mp3
add_hotkey('shift+ctrl+alt+d', wav_to_mp3)

# display hotkeys
show_hotkeys()

# run loop
keyboard.wait()
