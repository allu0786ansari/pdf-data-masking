from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from utils.text_extraction import extract_text_and_images
from utils.text_masking import mask_sensitive_info
from fpdf import FPDF

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Masked Data', 0, 1, 'C')

def save_text_as_pdf(text, pdf_path):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line.encode('latin1', 'replace').decode('latin1'))
    pdf.output(pdf_path)

@app.route('/')
def index():
    return render_template('upload.html', download_links=[])

@app.route('/uploader', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        download_links = []

        for f in files:
            file_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(file_path)
            
            # Process the PDF and mask sensitive info
            text = extract_text_and_images(file_path)
            print("Extracted text and images: ", text)
            masked_text = mask_sensitive_info(text)
            
            # Save the masked text as a new PDF file
            masked_pdf_path = os.path.join(PROCESSED_FOLDER, f.filename.replace('.pdf', '_masked.pdf'))
            save_text_as_pdf(masked_text, masked_pdf_path)
            
            download_links.append(url_for('download', filename=os.path.basename(masked_pdf_path)))
        
        return render_template('upload.html', download_links=download_links)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)