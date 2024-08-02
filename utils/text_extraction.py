from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from PIL import Image
import io
from .ocr import ocr_on_image

def extract_text_and_images(pdf_path):
    # Extract text from PDF
    pdf_reader = PdfReader(open(pdf_path, 'rb'))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_page = page.extract_text()
        if text_page:
            text += text_page + '\n'
    
    print("Text extracted from PDF:", text)

    # Extract images and perform OCR
    images = extract_images_from_pdf(pdf_path)
    for idx, image in enumerate(images):
        ocr_text = ocr_on_image(image)
        print(f"OCR text from image {idx+1}:", ocr_text)
        text += ocr_text + '\n'

    return text

def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
            print(f"Image {img_index+1} extracted from page {page_number+1}")
    return images