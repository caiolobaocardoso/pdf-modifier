import PyPDF2

path_pdf = "./test.pdf"

dados_pdf = open(path_pdf, "rb") 

pdf_reader = PyPDF2.PdfReader(dados_pdf)

len(pdf_reader.pages)
