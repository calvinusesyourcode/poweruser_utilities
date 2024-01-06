import datetime, time
import tkinter as tk
import pyperclip

def to_time(seconds):
    """Convert seconds to hh:mm:ss string, for use with ffmpeg."""
    return str(datetime.timedelta(seconds=seconds))

def get_clipboard():
    clipboard_text = pyperclip.paste()
    return clipboard_text

import tkinter as tk
import time

def show_message(message):
    # Create a new Tkinter window
    window = tk.Tk()
    window.configure(bg='black')
    window.overrideredirect(True)

    # Create a label with your message
    message_label = tk.Label(window, text=message, font=("TkFixedFont", 12), fg="white", bg="black")

    message_label.pack()
    window.update()

    window_width = message_label.winfo_reqwidth()
    window_height = message_label.winfo_reqheight()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    window.update()

    time.sleep(estimate_reading_time(message))
    window.destroy()


def estimate_reading_time(text):
    words_per_minute = 200
    words = text.split()
    num_words = len(words)
    minutes = num_words / words_per_minute
    # convert reading time to seconds
    seconds = minutes * 60
    return seconds

# def get_text_between(string, start_string, end_string):
#     start = string.find(start_string)
#     if start != -1: # the start string was found
#         start += len(start_string)
#         end = string.find(end_string, start)
#         if end != -1: # the end string was found
#             return string[start:end]
#     # if we reach here, one of the substrings was not found
#     return ''

# def epub_to_text(epub_path):
#     """Convert epub to text file."""
#     from epub2txt import epub2txt
#     return epub2txt(epub_path)

# print(get_text_between(epub_to_text("epub/waking_up.epub"), "For Annaka, Emma, and Violet", "Chapter 2"))
# # print((epub_to_text("epub/waking_up.epub")))

def godlike_copypaste():
    from pathlib import Path
    from sharing_is_caring import open_with_vscode
    directory = Path("C:\\Users\\calvi\\3D Objects\\test")
    directory.mkdir(parents=True, exist_ok=True)

    i = 0
    while True:
        file = directory / f"test{i}.py"
        if not file.exists():
            path = Path(str(directory)+"/"+f"test{i}.py")
            break
        i += 1

    with open(file, 'w') as f:
        f.write(pyperclip.paste())
    time.sleep(.5)
    open_with_vscode(directory)
    open_with_vscode(path)

def submit_to_sheets():
    body = {}
    i = 0
    while True:
        user_input = input("> ")
        if user_input == "":
            break
        else:
            body[i] = user_input
            i += 1
    for key in body:
        print("   ", key, body[key])
    time.sleep(2)


def notes_loop():
    print("> notes_loop\n")
    import os, datetime, subprocess

    def clear(): (os.system("cls") if os.name == "nt" else os.system("clear")); print("\n")
    def pretty_print(text): clear(); print(f"\n  {text}\n") 
    def look(path): subprocess.run(f"notepad {path}") if os.name == "nt" else subprocess.run(f"open {path}")
    
    notes_folder = "notes"
    os.makedirs(notes_folder, exist_ok=True)
    fdate = datetime.datetime.now().strftime("%Y%m%d")

    # fetch recent notes, sorted
    notes = [{"path":f} for f in os.listdir(notes_folder) if abs(int(fdate)-int(f[:8])) <= 14]
    for i, note in enumerate(notes):
        note["pretty_name"] = note["path"][9:].split('.')[0]
        with open(os.path.join(notes_folder, note["path"]), "r") as f:
            lines = f.read().splitlines()
            for line in lines[::-1]:
                note["last_opened"] = str(int(fdate)-30)
                if len(line) == 5:
                    note["last_opened"] = line.replace(":", "")
                    break
        
    notes = sorted(notes, key=lambda k: k["last_opened"], reverse=True)
    
    clear()
    session_name = None
    for i, note in enumerate(notes): print(f"  ({i}) {note['pretty_name']}")
    while session_name is None:
        session_name = input("\n# or new session_name: ")

    if session_name.isdigit():
        session_path = os.path.join(notes_folder, notes[int(session_name)]["path"])
        session_name = notes[int(session_name)]["pretty_name"]
    else:
        session_path = os.path.join(notes_folder, f"{fdate}-{session_name.replace(' ', '_')}.txt")

    if not os.path.exists(session_path):
        with open(session_path, "w") as f:
            f.write(f"{fdate}\n\n")
    
    pretty_print(f"{session_name}")
    n = 0
    while True:
        user_input = input("> ")
        if user_input == "":
            if n == 0: os.remove(session_path)
            break
        if user_input == "open":
            look(session_path)
            continue
        if user_input == "del":
            os.remove(session_path)
            break
        with open(session_path, "a") as f:
            f.write("\n"+datetime.datetime.now().strftime("%H:%M")+"\n")
            f.write(user_input+"\n")
        n += 1
        # f.close()
    print("> exiting...")