import fitz  # PyMuPDF
import streamlit as st

def ExtractPDFText(pdf):
    content = ""
    try:
        # Open the PDF using PyMuPDF from uploaded bytes
        pdf_document = fitz.open(stream=pdf.read(), filetype="pdf")

        # Iterate through all pages and extract text
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text = page.get_text()
            content += text

        pdf_document.close()

    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")

    return content
