# Tesseract OCR
import pytesseract
from PIL import Image
import sys
from pdf2image import convert_from_path
import os
import io

# If you need to assign tesseract to path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Matthew\AppData\Local\Tesseract-OCR\tesseract.exe'

pdf_path = 'faz-graça/pdf-modifier/Untitled_06242024_100609.pdf'
output_filename = "results.txt"
pages = convert_from_path(pdf_path)
pg_cntr = 1

sub_dir = str("images/" + pdf_path.split('/')[-1].replace('.pdf','')[0:20] + "/")
if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)

for page in pages:
    if pg_cntr <= 20:
        filename = "pg_"+str(pg_cntr)+'_'+pdf_path.split('/')[-1].replace('.pdf','.jpg')
        page.save(sub_dir+filename)
        with io.open(output_filename, 'a+', encoding='utf8') as f:
            f.write(unicode("======================================================== PAGE " + str(pg_cntr) + " ========================================================\n")) # type: ignore
            f.write(unicode(pytesseract.image_to_string(sub_dir+filename)+"\n")) # type: ignore
            f.write(unicode("======================================================== ========================= ========================================================\n")) # type: ignore
        pg_cntr = pg_cntr + 1