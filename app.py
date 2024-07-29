from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from utils.text_extraction import extract_text_from_pdf
from utils.text_masking import mask_sensitive_info
from utils.image_processing import mask_text_in_image
from utils.ocr import extract_text_from_image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(file_path)
        
        # Process the PDF and mask sensitive info
        text = extract_text_from_pdf(file_path)
        masked_text = mask_sensitive_info(text)
        
        # Save the masked text as a new text file for simplicity
        masked_pdf_path = os.path.join(PROCESSED_FOLDER, f.filename.replace('.pdf', '_masked.txt'))
        with open(masked_pdf_path, 'w') as masked_file:
            masked_file.write(masked_text)
        
        download_link = url_for('download', filename=os.path.basename(masked_pdf_path))
        return render_template('upload.html', download_link=download_link)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
