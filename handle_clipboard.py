import pytesseract, pyperclip, os
from PIL import ImageGrab

def perform_ocr_on_clipboard():
    img = ImageGrab.grabclipboard()
    text = pytesseract.image_to_string(img)
    pyperclip.copy(text.strip())
    if os.name == 'nt':
        import winsound
        winsound.Beep(500, 100)
