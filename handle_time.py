import csv, time, threading
from collections import deque
from handle_system import show_console, hide_console, time_since_input, wipe
from datetime import datetime, timedelta

io_map = {
    "i":"in",
    "o":"out",
    "c":"comment",
    "d":"done",
    "b":"back"
}

interval = 120

def punch(io=None, activity=None, time=None):
    if time is None:
        time = datetime.now()
        
    if io is None:
        print("\n".join([f"{key} = {io_map[key]}" for key in io_map]))
        print("\n")
        io = input("> ")
    
    if not (io == "o" or io == "b"):
        activity = input("> ")
    
    
    if io in io_map:
        io = io_map[io]

    timestring = time.strftime('%Y-%m-%d__%H-%M-%S')
    data = [timestring, io, activity]

    with open('data/punchcard.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def show_last_n_lines(filename='data/punchcard.csv', n=10):
    with open(filename, 'r') as f:
        last_n_lines = deque(f, maxlen=n)
        for line in last_n_lines:
            print(line.strip())

def on_screen_timer():
    import tkinter as tk    

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
    from handle_time import punch
    global time_tracking, afk
    if not time_tracking:
        threading.Thread(target=afk_monitor, daemon=True).start()
        time_tracking = True
    afk = False
    punch()

def countdown(root, time_seconds, label):
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


def timer():
    import tkinter as tk
    # task_name = input("Enter the task name: ")
    task_name = "deep work"
    timer_minutes = int(float(input("Enter the time in hours: ")) * 60)
    color = "black"

    root = tk.Tk()
    root.title("tk_task_timer")
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.attributes('-alpha', 1.0)
    root.configure(background='blue')
    root.wm_attributes("-transparentcolor", "blue")
    root.attributes("-topmost", True)

    label_time = tk.Label(root, text="", font=("Consolas", 12), bg=color, fg="white")
    label_time.place(x=root.winfo_screenwidth() / 2, y=root.winfo_screenheight()*0.97, anchor='n')
    countdown(root, timer_minutes * 60, label_time)

    root.mainloop()