import os
import sys
import shutil
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract

def extract_name_from_text(text):
    """
    Attempt to find the line after 'This is to certify that' or 'This certifies'.
    This covers Edexcel and Cambridge certificates, just modify the ``key_phrases`` list as you see fit
    If these all fail, we fallback to looking for the largest uppercase line.
    """
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    key_phrases = ['this is to certify that', 'this certifies']

    # Look for key phrase that signifies name on next line
    for i, line in enumerate(lines):
        for exp in key_phrases:
            if exp in line.lower():
                if i + 1 < len(lines):
                    return lines[i + 1]

    # Fallback: pick the first line that is mostly uppercase
    uppercase_candidates = [l for l in lines if l.isupper() and len(l.split()) > 1]
    if uppercase_candidates:
        return uppercase_candidates[0]
    
    # Just return something
    return "UnknownName"

def prompt_examining_body():
    """
    Prompt user to enter 'C' or 'E'. Keep asking until
    a valid value is entered.
    """
    body_codes = {
        'C' : 'Cambridge',
        'E' : 'Edexcel',
        'OCR' : 'OCR',
        'OX' : 'Oxford',
        'AQA' : 'AQA'
    }
    while True:
        print("Enter examining body code:")
        for code, name in body_codes.items():
            print(f"  {code} for {name}")
        
        user_choice = input("Your choice: ").strip().upper()
        
        if user_choice in body_codes.keys():
            return body_codes[user_choice]
    
        print("Invalid choice. Please try again.\n")

def prompt_level():
    """
    Prompt user to enter qualification code. Keep asking until
    a valid value is entered.
    """
    level_codes = {
            'G' : 'GCSE',
            'IG' : 'IGCSE',
            'IAS' : 'IAS_level',
            'IA' : 'IA_level',
            'AS' : 'AS_level',
            'A' : 'A_level'
    }

    while True:
        print("Enter examination level code:")
        for code, name in level_codes.items():
            print(f"  {code} for {name}")
        
        user_choice = input("Your choice: ").strip().upper()
        
        if user_choice in level_codes.keys():
            return level_codes[user_choice]
    
        print("Invalid choice. Please try again.\n")

def prompt_year():
    while True:
        user_year = input("Enter examination year YYYY: ")

        if user_year.isdigit():
            if int(user_year) > 2000 and int(user_year) < 2100:
                return int(user_year)
        
        print("Invalid year. Please try again.")

def prompt_window():

    window_codes = {
        "Jun" : "June",
        "Jan" : "January",
        "Oct" : "October"
     }

    while True:
        print("Enter examination window: ")
        for code, name in window_codes.items():
            print(f"  {code} for {name}")
        
        user_choice = input("Your choice: ").strip()
        
        if user_choice in window_codes.keys():
            return window_codes[user_choice]
    
        print("Invalid choice. Please try again.\n")

def split_and_ocr(input_pdf_path, examining_body, level, year, window):
    # 1) Create a folder named after the PDF (without .pdf)
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    output_folder = base_name
    os.makedirs(output_folder, exist_ok=True)

    # 2) Read the PDF
    pdf_reader = PdfReader(input_pdf_path)
    total_pages = len(pdf_reader.pages)

    # 3) For each page, do OCR & save
    for page_number in range(total_pages):
        single_page_writer = PdfWriter()
        single_page_writer.add_page(pdf_reader.pages[page_number])

        # Temporary single-page PDF
        temp_pdf_path = os.path.join(output_folder, f"temp_page_{page_number}.pdf")
        with open(temp_pdf_path, "wb") as temp_file:
            single_page_writer.write(temp_file)

        # Convert to image
        images = convert_from_path(temp_pdf_path)
        text = pytesseract.image_to_string(images[0]) if images else ""

        # Extract name
        student_name = extract_name_from_text(text)
        if not student_name:
            student_name = f"Certificate_Page_{page_number+1}"

        # Clean name for filenames
        safe_name = student_name.replace(' ', '_')

        # 4) Construct final PDF filename
        output_pdf_name = f"{safe_name}-{examining_body}-{level}-{window}-{year}.pdf"
        output_pdf_path = os.path.join(output_folder, output_pdf_name)

        # Write the final single-page PDF
        with open(output_pdf_path, "wb") as final_file:
            single_page_writer.write(final_file)

        # Remove temp PDF
        os.remove(temp_pdf_path)

        print(f"Page {page_number+1}/{total_pages} => {output_pdf_name}")
    zip_path = shutil.make_archive(output_folder, 'zip', output_folder)
    print(f"Zipped folder: {zip_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf>")
        sys.exit(1)

    input_pdf_path = sys.argv[1]

    # Check file exists where it should
    if not os.path.exists(input_pdf_path):
        print(f"Error: The file '{input_pdf_path}' does not exist.")
        sys.exit(1)
    
    # Continue with the rest of your logic here...
    print(f"Processing file: {input_pdf_path}")

    # Prompt the user
    examining_body = prompt_examining_body()
    level = prompt_level()
    year = prompt_year()
    window = prompt_window()

    split_and_ocr(input_pdf_path, examining_body, level, year, window)

if __name__ == "__main__":
    main()
