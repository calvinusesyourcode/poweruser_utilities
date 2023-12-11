import tkinter as tk
import time

def countdown(time_seconds, label):
    while time_seconds > -1:
        mins, secs = divmod(time_seconds, 60)
        print(mins, secs)
        hours, mins = divmod(mins, 60)
        print(hours, mins, secs)
        if hours >= 1:
            timer = ' {} — {:02d}:{:02d}:{:02d} '.format(task_name, hours, mins, secs)
        else:
            timer = ' {} — {:02d}:{:02d} '.format(task_name, mins, secs)
        label.config(text=timer)
        root.update()
        time.sleep(1)
        time_seconds -= 1

# task_name = input("Enter the task name: ")
timer_minutes = int(float(input("Enter the time in hours: ")) * 60)
task_name = "deep work"
color = "black"

root = tk.Tk()
root.title("Task Timer")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes('-alpha', 1.0)
root.configure(background='blue')
root.wm_attributes("-transparentcolor", "blue")
root.attributes("-topmost", True)

thickness = 5
rects = [
    tk.Frame(root, bg=color, height=thickness),
    tk.Frame(root, bg=color, height=thickness),
    tk.Frame(root, bg=color, width=thickness),
    tk.Frame(root, bg=color, width=thickness)
]
for rect in rects:
    rect.pack(side=rects.index(rect) % 2 and 'left' or 'top', fill='both')

label_time = tk.Label(root, text="", font=("Consolas", 12), bg=color, fg="white")
label_time.place(x=root.winfo_screenwidth() / 2, y=root.winfo_screenheight()*0.97, anchor='n')
countdown(timer_minutes * 60, label_time)

root.mainloop()
