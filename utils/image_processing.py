import cv2
import pytesseract

def mask_text_in_image(image_path):
    image = cv2.imread(image_path)
    d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
    masked_image_path = 'masked_' + image_path
    cv2.imwrite(masked_image_path, image)
    return masked_image_path
