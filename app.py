import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import re
from datetime import date
import base64

def base_64_background(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = base_64_background(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def perform_ocr(image):
    return pytesseract.image_to_string(image)

def extract_info(text):
    name_match = re.search(r'Nome\s+(.*?)\s+E-mail', text, re.IGNORECASE | re.DOTALL)
    id_match = re.search(r'ID\s+(.*?)\s+Cargo', text, re.IGNORECASE | re.DOTALL)
    
    name = name_match.group(1).strip() if name_match else "Not found"
    id_value = id_match.group(1).strip() if id_match else "Not found"

    return name, id_value

def process_file(uploaded_file):
    images = convert_from_bytes(uploaded_file.read())
    full_text = ""
    for i, image in enumerate(images):
        st.subheader(f"Página {i+1} - {uploaded_file.name}")
        st.image(image, caption=f"Página {i+1}", use_column_width=True)
        
        text = perform_ocr(image)
        full_text += text + "\n\n"
        
        st.text_area(f"Texto Extraído - Página {i+1} - {uploaded_file.name}", text, height=250)

    name, id_value = extract_info(full_text)

    st.subheader(f"Informações Extraídas - {uploaded_file.name}")
    st.write(f"Nome: {name}")
    st.write(f'ID: {id_value}')
    
    data = date.today()
    new_file_name = f'{name}-{id_value}-{data}.pdf'
    
    st.download_button(
        label=f"Baixar PDF Renomeado - {uploaded_file.name}",
        data=uploaded_file.getvalue(),
        file_name=new_file_name,
        mime="application/pdf"
    )

def main():

    st.set_page_config(page_title="Extrator de PDF", page_icon="📄", layout="wide")
    
    set_background('background.jpg')
    
    st.markdown("""
    <style>
        .main-title {
            color: #8E24AA;
            text-align: center;
            padding-top: 20px;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            background-color: #ffffff;
        }
        .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Extrator de PDF</h1>", unsafe_allow_html=True)

    
    uploaded_files = st.file_uploader("Escolha um ou mais arquivos PDF", type="pdf", accept_multiple_files=True)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            process_file(uploaded_file)

if __name__ == "__main__":
    main()
