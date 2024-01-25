import PyPDF2

def parsing(pdf_reader):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extractText()
    return text