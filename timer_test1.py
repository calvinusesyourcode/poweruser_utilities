import tkinter as tk
import time

def stopwatch(label):
    time_seconds = 0
    while True:
        mins, secs = divmod(time_seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours >= 1:
            timer = ' {} — {:02d}:{:02d}:{:02d} '.format(task_name, hours, mins, secs)
        else:
            timer = ' {} — {:02d}:{:02d} '.format(task_name, mins, secs)
        label.config(text=timer)
        root.update()
        time.sleep(1)
        time_seconds += 1

def toggle_label(event):
    if event.y <= 3:
        label_time.place(x=root.winfo_screenwidth() / 2, y=0, anchor='n')
    else:
        label_time.place_forget()

# Get User Inputs
task_name = input("Enter the task name: ")
color = "black"

# Create Main Window
root = tk.Tk()
root.title("Task Timer")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes('-alpha', 1.0)
root.configure(background='blue')
root.wm_attributes("-transparentcolor", "blue")
root.attributes("-topmost", True)

# Create 4 Thin Rectangles for Border
thickness = 5
rects = [
    tk.Frame(root, bg=color, height=thickness),
    tk.Frame(root, bg=color, height=thickness),
    tk.Frame(root, bg=color, width=thickness),
    tk.Frame(root, bg=color, width=thickness)
]
rects[0].pack(side='top', fill='both')
rects[1].pack(side='bottom', fill='both')
rects[2].pack(side='left', fill='both')
rects[3].pack(side='right', fill='both')

# Display Task Name and Timer on the Same Line with 50% Smaller Font
label_time = tk.Label(root, text="", font=("Consolas", 12), bg=color, fg="white")

# Bind mouse motion event to toggle_label function
root.bind('<Motion>', toggle_label)

stopwatch(label_time)

root.mainloop()