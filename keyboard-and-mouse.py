from pynput import mouse
import keyboard
import time


def on_click(x, y, button, pressed):
    global previous_click_time, time_difference
    if pressed and button == mouse.Button.left:
        click_time = time.time()
        if previous_click_time is not None:
            time_difference = click_time - previous_click_time
        previous_click_time = click_time
        mouse_history.append(("left", time_difference, [x,y]))
        print(f"Mouse clicked at position ({x}, {y}) after {time_difference} seconds")


def on_scroll(x, y, dx, dy):
    if mouse_history[-1][0] == "scroll":
        mouse_history[-1][2][0] += dx
        mouse_history[-1][2][1] += dy
    else:
        mouse_history.append(("scroll", [x, y], [dx, dy] ))
    print(f"Mouse scrolled at position ({x}, {y}) with delta ({dx}, {dy})")


def get_clicks(run_name):
    """Creates array [(seconds, x, y)] and returns yaml file
    location and key of the array now stored within."""
    global previous_click_time, time_difference, mouse_history
    mouse_history = []
    previous_click_time = None
    time_difference = None

    print("Waiting for Ctrl + Alt + Shift + G...")
    keyboard.wait("ctrl+alt+shift+g")
    print("Key combination detected. Begins with first click.")

    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
        keyboard.wait("ctrl+alt+shift+g")
        listener.stop()
        for event in mouse_history:
            print(event)

get_clicks("test")
