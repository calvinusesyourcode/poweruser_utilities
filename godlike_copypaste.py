import tkinter as tk
from pathlib import Path
import subprocess, time
from sharing_is_caring import open_with_vscode

# Get the content from the clipboard
root = tk.Tk()
root.withdraw()  # Hide the tkinter window
clipboard_content = root.clipboard_get()

# Define the directory for the new Python file
directory = Path("C:\\Users\\calvi\\3D Objects\\test")

# Ensure the directory exists
directory.mkdir(parents=True, exist_ok=True)

# Find an available file name
i = 0
while True:
    file = directory / f"test{i}.py"
    if not file.exists():
        path = Path(str(directory)+"/"+f"test{i}.py")
        break
    i += 1

# Write the clipboard content to the new Python file
with open(file, 'w') as f:
    f.write(clipboard_content)
time.sleep(.5)
open_with_vscode(path)