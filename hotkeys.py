import keyboard, time, os, threading, typing, sys
from handle_windows10 import show_console, hide_console

# lock = threading.Lock()
f3d = "C:/Users/calvi/3D Objects"

def run_app(app: typing.Callable):
# with lock:
    show_console()
    os.system("cls")
    app()
    hide(3)


def hide(seconds: int):
    for i in range(seconds, 0, -1):
        print(f" > closing in {i}", end='\r')
        time.sleep(1)
    hide_console()

# def exit(seconds: int):
# # with lock:
#     show_console()
#     for i in range(seconds, 0, -1):
#         print(f" > exiting in {i}", end='\r')
#         time.sleep(1)
#     hide_console()
#     sys.exit()

from handle_youtube import download_with_ui
keyboard.add_hotkey('shift+ctrl+alt+y', lambda: run_app(download_with_ui))
from handle_audio import to_mp3_with_ui, audio_to_audio_with_ui, trim_audio_with_ui

# keyboard.add_hotkey('shift+ctrl+alt+k', lambda: exit(3))
print("added hotkeys")
time.sleep(0.250)
hide_console()
keyboard.wait()

# keyboard.add_hotkey('shift+ctrl+alt+k', lambda: run_app(r'C:\Users\calvi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\PanoramaStudio 3 Pro.lnk'))
# keyboard.add_hotkey('shift+ctrl+alt+h', lambda: run_app(f'{f3d}/poweruser_utilities/ableton_demo_creater.py'))
# keyboard.add_hotkey('shift+ctrl+alt+u', lambda: run_app(f'{f3d}/poweruser_utilities/trim_audio_with_ui.py'))
# keyboard.add_hotkey('shift+ctrl+alt+t', lambda: run_app(f'{f3d}/poweruser_utilities/to_mp3_with_ui.py'))
# keyboard.add_hotkey('shift+ctrl+alt+i', lambda: run_app(f'{f3d}/poweruser_utilities/to_audio_with_ui.py'))