import fitz

def extract_clean_text_from_pdf(file_path):
    """
    주어진 PDF 파일 경로에서 텍스트를 추출하고 정제합니다.
    """
    doc = fitz.open(file_path)  # PDF 파일 열기
    text = ""
    for page in doc:  # 각 페이지에 대해
        text += page.get_text().replace("\n", "").replace("-", "").replace('\x0c', '').replace('  ', ' ')  # 텍스트 추출 후 정제
    doc.close()
    return text

def debug_load_file(bill_no: int):
    if exist_bill_metadata(bill_no):
        doc = fitz.open(f"{os.getenv('BILL_PDF_LOCATION')}/{bill_no}.pdf")