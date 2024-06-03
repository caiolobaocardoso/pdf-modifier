import PyPDF2

class first_page():
    def pagina_1():
        pdf_file_object = open(r"C:\Users\accbe\OneDrive\Área de Trabalho\workspace\pdf-modifier\Untitled_05212024_134727.pdf", "rb")
        pdf_reader_object = PyPDF2.PdfReader(pdf_file_object)
        first_page_object = pdf_reader_object.pages[0]
        print(first_page_object.extract_text())

first_page.pagina_1()
