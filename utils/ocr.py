import pytesseract
from PIL import Image

def ocr_on_image(image):
    text = pytesseract.image_to_string(image)
    return text
