import keyboard, time, os, typing 
from handle_windows10 import show_console, hide_console
hide_console()

f3d = "C:/Users/calvi/3D Objects"
hotkeys = {}

def run(app: typing.Callable):
    show_console()
    os.system("cls")
    app()
    hide(3)

def hide(seconds: int):
    for i in range(seconds, 0, -1):
        print(f"  > closing in {i}", end='\r')
        time.sleep(1)
    hide_console()

def add_hotkey(hotkey: str, app: typing.Callable):
    keyboard.add_hotkey(hotkey, lambda: run(app))
    hotkeys[hotkey.split("+")[-1]] = str(app.__name__)

# add hotkeys
from handle_youtube import download_with_ui
add_hotkey('shift+ctrl+alt+y', download_with_ui)

from handle_strings import godlike_copypaste, submit_to_sheets
from handle_twitter import tweet
add_hotkey('shift+ctrl+alt+b', godlike_copypaste)
add_hotkey('shift+ctrl+alt+a', submit_to_sheets)
add_hotkey('shift+ctrl+alt+s', tweet)


# from handle_audio import to_mp3_with_ui, audio_to_audio_with_ui, trim_audio_with_ui
# keyboard.add_hotkey('shift+ctrl+alt+t', lambda: run())
# keyboard.add_hotkey('shift+ctrl+alt+u', lambda: run())
# keyboard.add_hotkey('shift+ctrl+alt+i', lambda: run())

from ableton_demo_creater import wav_to_mp3
add_hotkey('shift+ctrl+alt+d', wav_to_mp3)

# display hotkeys and run main loop
show_console()
print("added hotkeys")
time.sleep(0.250)
print("\n")

sorted_hotkeys = {k: hotkeys[k] for k in sorted(hotkeys)}
for key in sorted_hotkeys:
    print("    ", key, sorted_hotkeys[key])
print("\n")
hide(1)
keyboard.wait()
