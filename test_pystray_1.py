import pystray
from PIL import Image, ImageDraw

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def on_activate(icon, item):
    print("Taskbar icon clicked!")

image = create_image(64, 64, 'black', 'blue')
icon = pystray.Icon("test_icon", image, "My System Tray Icon", menu=pystray.Menu(pystray.MenuItem('Option 1', on_activate)))

icon.run()
