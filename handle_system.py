import ctypes, time, os

def hide_console():
    if os.name == "nt":
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd:
            ctypes.windll.user32.ShowWindow(hWnd, 0)
    else:
        print("> fix hide_console()")

def show_console():
    wipe()
    if os.name == "nt":
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd:
            set_console_size(400, 300)
            ctypes.windll.user32.ShowWindow(hWnd, 1)
            time.sleep(0.100)
            ctypes.windll.user32.SetForegroundWindow(hWnd)
    else:
        print("> fix show_console()")


def set_console_size(width, height):
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hWnd, ctypes.byref(rect))
        ctypes.windll.user32.MoveWindow(hWnd, rect.left, rect.top, width, height, True)

def time_since_input():
    if os.name == "nt":
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
        return ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    else:
        print("> fix idle_checking()")

def wipe():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

