import PyPDF2
from PyPDF2.errors import PdfReadError

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except PdfReadError:
        raise ValueError("Error reading PDF. The file might be corrupted or not a valid PDF.")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred while processing the PDF: {e}")

