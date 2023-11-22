import pytesseract, pyperclip, os, keyboard
from PIL import ImageGrab

def perform_ocr_on_clipboard():
    img = ImageGrab.grabclipboard()
    text = pytesseract.image_to_string(img)
    pyperclip.copy(text.strip())
    if os.name == 'nt':
        import winsound
        winsound.Beep(500, 100)

def fix_windows_file_path_on_clipboard():
    current_clipboard_content = pyperclip.paste()
    fixed_path = current_clipboard_content.replace('\\', '\\\\')
    pyperclip.copy(fixed_path)
    if os.name == 'nt':
        import winsound
        winsound.Beep(500, 100)

def type_clipboard_contents():
    keyboard.write(pyperclip.paste(), delay=0.050)