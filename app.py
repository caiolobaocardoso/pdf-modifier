from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract

# Converte o arquivo pdf em imagem

path_pdf = "./Untitled_05212024_134727.pdf"
pages = convert_from_path(path_pdf)

# Função de pré-processamento das imagens

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

#Realiza processo de OCR nas imagens processadas

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

#Lista que irá armazenar o conteúdo do texto
extracted_text = []

for page in pages:
    #Realiza o pré-processamento das imagens
    preprocessed_image = deskew(np.array(page))

    # Extração do texto usando OCR
    text = extract_text_from_image(preprocessed_image)
    extracted_text.append(text)

print(text)