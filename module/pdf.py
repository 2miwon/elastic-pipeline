def parsing_pdf_text(pdf_content: bytes):
    import io
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def parsing_pdf_metadata(pdf_content: bytes):
    import io
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    metadata = pdf_reader.metadata
    return metadata

