import requests
from bs4 import BeautifulSoup
import copy

from config import *
from metadata import *
# from Module import *

basic_param = {
    "KEY": os.getenv('ASSEMBLY_OPENAPI_KEY'),
    "Type": "json"
}
numbering_start = [("010002", "010299"), #제헌
                   "020001", #제2대
                   "030001", #제3대
                   "040035", #제4대
                   ("2100001", )]

#
# url 구성
#

def openAPI_url_config(code: str, parameter: dict) -> str:
    """
    openAPI 요청 url 구성
    """
    url = OPENAPI_BASIC_URL + code + '?'
    for param, value in parameter.items():
        url += param + '=' + value + '&'
    return url

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
# OpenAPI 상호작용
#

def get_bill_api_data(pIndex: int) -> str:
    param = copy.deepcopy(basic_param)
    # param["BILL_NO"] = str(bill_no)
    param['pIndex'] = str(pIndex)
    param['pSize'] = "1"
    response = requests.get(openAPI_url_config(OPENAPI_SEARCH_BILL_CODE ,param))
    if response.status_code == 200:
        if OPENAPI_SEARCH_BILL_CODE not in response.json():
            return None, None
        
        content_json = response.json()[OPENAPI_SEARCH_BILL_CODE]
        return parsing_json(content_json)
    else:
        raise Exception("Fail to request API")
    
def parsing_json(json: dict) -> str:
    if json[0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
        body = json[1]['row']
        return body[0]['BILL_NO'], body[0]['BILL_ID']
    else:
        return None

#
# 의안정보시스템 웹사이트 상호작용 (BS4)
# 
    
# /html/body/div/div[2]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[4]/a[2]
def get_bill_origin_file_link(billId: str) -> str:
    link = get_bill_info_system_url(billId)
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
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
            bill_no, bill_id = get_bill_api_data(i)
            if bill_no is None:
                break
            # if not read_bill_metadata_by_bill_no(bill_no):
            if not os.path.exists(os.getenv('BILL_PDF_LOCATION') + bill_no + ".pdf"):
                file_link = get_bill_origin_file_link(bill_id)
                file_name = bill_no + ".pdf"
                download_file(file_link, os.getenv('BILL_PDF_LOCATION'), file_name)
                insert_bill_metadata(bill_no, bill_id, file_link)
                print(f"Success to download file {file_name}")
        except Exception as e:
            print(f"Fail to download file: {e}")