# OCR Certificates Project

This Python script takes a **multi-page PDF** of scanned certificates and:

1. Splits it into individual PDF pages  
2. Extracts each student’s name via OCR  
3. Renames each page’s PDF to `"{name}-{examBody}-{level}-{window}-{year}.pdf"`
4. Zips up all the resulting PDFs into a single archive  

---

## Features

- **User Prompts:**
  - Prompts for the examining body (e.g., Cambridge, Edexcel, etc.)
  - Prompts for level (IGCSE, AS, or A, etc.)
  - Allows you to easily store relevant data in the output filenames

- **OCR with Tesseract:**
  - Extracts the name from certificate text
  - You can customize how it detects the name based on your certificate layout

- **Output:**
  - Creates a folder named after the original PDF file (minus the extension)
  - Inside that folder, each single-page PDF is saved with the student’s name, examining body, level,git statyus year of examination, and exam window in the filename
  - At the end, it automatically creates a ZIP file of the entire folder for easy download or sharing

---

## Requirements

- **Python 3+**
- **PyPDF2** for PDF manipulation
- **pdf2image** for converting PDF pages to images
- **pytesseract** for OCR
- **Tesseract OCR** installed on your system (so `pytesseract` can call it)
- **Poppler** installed (for `pdf2image` to run `pdfinfo` and convert PDFs to images)

### Installing Dependencies

If you have a `requirements.txt` file, you can install the Python dependencies with:

```bash
pip install -r requirements.txt
