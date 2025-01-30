from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def save_summary_to_pdf(summary: str, filename: str):
    # Define the PDF file name
    pdf_filename = f"summary_{filename}.pdf"
    
    # Create a canvas to generate the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Add the summary text to the PDF
    c.drawString(100, 750, "Summary:")
    text = c.beginText(100, 730)
    text.setFont("Helvetica", 10)
    text.setTextOrigin(100, 730)
    text.textLines(summary)
    
    c.drawText(text)
    c.showPage()
    c.save()

    return pdf_filename
