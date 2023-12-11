import time, os, typing, threading, sys, importlib

apps = []
entries = []
dir = os.path.dirname(os.path.realpath(__file__))
hotscriptsdir = dir+"\\hotscripts\\"
os.makedirs(hotscriptsdir, exist_ok=True)
ahkheader = """
#Requires AutoHotkey v2.0
#Warn
SetWorkingDir A_WorkingDir
#SingleInstance
"""
pyheader = """
import os

"""
autohotkeymap = {
    "shift": "+",
    "ctrl": "^",
    "alt": "!",
    "win": "#",
}

def add_hotkey(hotkey: str, app: typing.Callable):
    apps.append({
        "hotkey": hotkey,
        "module": app.__module__,
        "app": app.__name__,
    })

# add hotkeys
from handle_assistant import ffmpeg_assist
add_hotkey('ctrl+shift+alt+f', ffmpeg_assist)

from handle_time import show_last_n_lines, punch_and_start_afk_monitoring
add_hotkey('ctrl+shift+alt+a', punch_and_start_afk_monitoring)
add_hotkey('ctrl+shift+alt+w', show_last_n_lines)

from handle_clipboard import perform_ocr_on_clipboard, fix_windows_file_path_on_clipboard, type_clipboard_contents
add_hotkey('ctrl+shift+alt+l', perform_ocr_on_clipboard)
add_hotkey('ctrl+shift+alt+[', fix_windows_file_path_on_clipboard)
add_hotkey('ctrl+shift+alt+v', type_clipboard_contents)

from handle_youtube import download_with_ui, download_transcript_with_ui
add_hotkey('ctrl+shift+alt+y', download_with_ui)
add_hotkey('ctrl+shift+alt+t', download_transcript_with_ui)

from handle_strings import godlike_copypaste, submit_to_sheets
from handle_twitter import tweet
add_hotkey('ctrl+shift+alt+b', godlike_copypaste)
add_hotkey('ctrl+shift+alt+s', tweet)

from ableton_demo_creater import wav_to_mp3
add_hotkey('ctrl+shift+alt+d', wav_to_mp3)

for app in apps:
    app['hotkey'] = "".join([autohotkeymap[c] if c in autohotkeymap.keys() else c for c in app['hotkey'].split("+")])
    scriptpath = f"{hotscriptsdir}{app['module']}--{app['app']}.py"
    entries.append(f'{app["hotkey"]}::{"{"}\n    Run "{scriptpath}"\n    return\n{"}"}\n')
    with open(scriptpath, "w") as f:
        f.write(f"""from {app['module']} import {app['app']}\n{app['app']}()""")

with open("poweruser_utilities.ahk", "w") as f:
    f.write(ahkheader)
    for entry in entries:
        f.write(entry)

    