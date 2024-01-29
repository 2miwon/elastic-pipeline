from bs4 import BeautifulSoup
from .open_api import *
from config import *
from database import *

def get_bill_info_system_url(billId: str) -> str:
    url = ASSEMBLY_BILL_INFO_BASIC_URL + "billId=" + billId
    return url

def pdf_url_config(bookId: str, Type="1") -> str:
    """
    pdf 파일 다운로드용 url
    한글 파일은 type = 0 / pdf 파일은 type = 1
    """
    url = ASSEMBLY_PDF_BASIC_URL + "?bookId=" + bookId + "&type=" + Type
    return url

#
# 의안정보시스템 웹사이트 상호작용 (BS4)
# 
    
# /html/body/div/div[2]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[4]/a[2]
def get_bill_origin_file_link(billId: str) -> str:
    link = get_bill_info_system_url(billId)
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # table = soup.find('table')
        # parsed = table.select_one(BILL_ORIGIN_TABLE_XPATH)
        parsed = soup.select_one(BILL_ORIGIN_XPATH)
        if parsed is None:
            raise Exception("There are no file")
        book_id = inner_book_id_parser(parsed.get('href'))
        return pdf_url_config(book_id)
    else:
        raise Exception(f"Fail to request {link} with status code {response.status_code}")

def inner_book_id_parser(href: str) -> str:
    param = href.split(",")[1]
    return param.split("'")[1]

def request_pdf(pdf_url: str):
    response = requests.get(pdf_url)
    pdf_content = response.content
    return pdf_content

def get_bill_origin_file_name(link: str) -> str:
    return link.split("=").split("&")[0]

#
# 파일 다운로드
#

def download_file(url: str, file_path: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(file_path, file_name), 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Fail to download file from {url} with status code {response.status_code}")

def loading_file():
    for i in range(1, 100000):
        try:
            bill_no, bill_id, title = get_bill_api_data(i)
            if bill_no is None:
                break
            # if not read_bill_metadata_by_bill_no(bill_no):
            if not os.path.exists(os.path.abspath(os.getenv('BILL_PDF_LOCATION')) + "/" + bill_no + ".pdf"):
                file_link = get_bill_origin_file_link(bill_id)
                file_name = bill_no + ".pdf"
                download_file(file_link, os.getenv('BILL_PDF_LOCATION'), file_name)
                insert_bill_metadata(bill_no, bill_id, file_link, title)
                print(f"Success to download file {file_name}")
        except Exception as e:
            print(f"Fail to download file: {e}")

if __name__ == "__main__":
    loading_file()