import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import re

def perform_ocr(image):
    return pytesseract.image_to_string(image)

def extract_info(text):
    name_match = re.search(r'Nome\s+(.*?)\s+E-mail', text, re.IGNORECASE | re.DOTALL)
    email_match = re.search(r'E-mail\s+(.*?)$', text, re.IGNORECASE | re.MULTILINE)
    
    name = name_match.group(1).strip() if name_match else "Not found"
    email = email_match.group(1).strip() if email_match else "Not found"
    
    return name, email

def main():
    st.title("PDF OCR Extractor")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read())
        full_text = ""
        for i, image in enumerate(images):
            st.subheader(f"Page {i+1}")
            
            st.image(image, caption=f"Page {i+1}", use_column_width=True)
            
            text = perform_ocr(image)
            full_text += text + "\n\n"
            
            st.text_area(f"Extracted Text - Page {i+1}", text, height=250)

        name, email = extract_info(full_text)

        st.subheader("Extracted Information")
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")

if __name__ == "__main__":
    main()