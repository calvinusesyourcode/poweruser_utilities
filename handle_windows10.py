import ctypes

def hide_console():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        ctypes.windll.user32.ShowWindow(hWnd, 0)

def show_console():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        set_console_size(400, 300)
        ctypes.windll.user32.ShowWindow(hWnd, 1)

def set_console_size(width, height):
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hWnd, ctypes.byref(rect))
        ctypes.windll.user32.MoveWindow(hWnd, rect.left, rect.top, width, height, True)
