# display tkinter window and then kill 3 seconds later

import tkinter as tk
import time

root = tk.Tk()
root.title("console")
root.geometry("300x200")
root.mainloop()
time.sleep(3)
root.withdraw()
root.destroy()