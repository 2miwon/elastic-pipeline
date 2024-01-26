import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import copy
from config import *

from pdf_parser import *
from Module import byte_json2dict

load_dotenv(verbose=True)
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
    print(url)
    return url

def get_bill_info_system_url(billId: str) -> str:
    return ASSEMBLY_BILL_INFO_BASIC_URL + "billId=" + billId

def pdf_url_config(bookId: str, Type="1") -> str:
    """
    pdf 파일 다운로드용 url
    한글 파일은 type = 0 / pdf 파일은 type = 1
    """
    return ASSEMBLY_PDF_BASIC_URL + "?bookId=" + bookId + "&type=" + Type

#
# OpenAPI 상호작용
#

# def get_lastest_bill_num() -> str:
#     param = copy.deepcopy(basic_param)
#     # param['pIndex'] = "1"
#     param['pSize'] = "1"
#     response = requests.get(openAPI_url_config(os.getenv('OPENAPI_SEARCH_BILL_CODE') ,param))
#     if response.status_code == 200:
#         content_json = response.json()[os.getenv('OPENAPI_SEARCH_BILL_CODE')]
#         return parsing_json_bill_num(content_json)
#     else:
#         raise("Fail to request API")

# def parsing_json_bill_num(json: dict) -> str:
#     if json[0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
#         body = json[1]['row']
#         return body[0]['BILL_NO']
#     else:
#         return None

def get_bill_id(pIndex: int) -> str:
    param = copy.deepcopy(basic_param)
    # param["BILL_NO"] = str(bill_no)
    param['pIndex'] = str(pIndex)
    param['pSize'] = "1"
    response = requests.get(openAPI_url_config(OPENAPI_SEARCH_BILL_CODE ,param))
    if response.status_code == 200:
        if OPENAPI_SEARCH_BILL_CODE not in response.json():
            return None
        
        content_json = response.json()[OPENAPI_SEARCH_BILL_CODE]
        return parsing_json_bill_id(content_json)
    else:
        raise("Fail to request API")
    
def parsing_json_bill_id(json: dict) -> str:
    if json[0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
        body = json[1]['row']
        return body[0]['BILL_ID']
    else:
        return None

#
# 의안정보시스템 웹사이트 상호작용 (BS4)
# 

def get_bill_info_system_html(billId: str) -> str:
    response = requests.get(get_bill_info_system_url(billId))
    if response.status_code == 200:
        return response.text
    else:
        raise("Fail to request html")

def request_pdf(pdf_url: str):
    response = requests.get(pdf_url)
    pdf_content = response.content
    print(type(pdf_content))

# request_pdf()

# ','5985B17F-6EB7-94FE-3648-67511E646665','1')

# function openBillFile(baseurl, bookid, type) {
# 	var url = baseurl+"?bookId="+escape(bookid)+"&type="+escape(type);
# 	$("#hiddenForm").attr("action", url);
# 	$("#hiddenForm").submit();
# }