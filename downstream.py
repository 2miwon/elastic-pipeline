import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import copy

from pdf_parser import *
from Module import byte_json2dict

load_dotenv(verbose=True)
basic_param = {
    "KEY": os.getenv('ASSEMBLY_OPENAPI_KEY'),
    "Type": "json"
}
numbering_start = 2100001

#
# url 구성
#

def openAPI_url_config(code: str, parameter: dict) -> str:
    """
    openAPI 요청 url 구성
    """
    url = os.getenv('OPENAPI_BASIC_URL') + code + '?'
    for param, value in parameter.items():
        url += param + '=' + value + '&'
    print(url)
    return url

def get_bill_info_system_url(billId: str) -> str:
    return os.getenv('ASSEMBLY_BILL_INFO_BASIC_URL') + "billId=" + billId

def pdf_url_config(bookId: str, Type="1") -> str:
    """
    pdf 파일 다운로드용 url
    한글 파일은 type = 0 / pdf 파일은 type = 1
    """
    return os.getenv('ASSEMBLY_PDF_BASIC_URL') + "?bookId=" + bookId + "&type=" + Type

#
# OpenAPI 상호작용
#

def request_API_bill_info():
    # param["BILL_NO"] = str(bill_no)
    param = copy.deepcopy(basic_param)
    param['pIndex'] = "1"
    param['pSize'] = "1"
    response = requests.get(openAPI_url_config(os.getenv('OPENAPI_SEARCH_BILL_CODE') ,param))
    if response.status_code == 200:

    else 
        raise 
    content = response.json()
    # if response.content[os.getenv('OPENAPI_SEARCH_BILL_CODE')]:
    #     pass
    print(byte_json2dict(response.content))
    return response.content

#
# 의안정보시스템 웹사이트 상호작용 (BS4)
# 




print(request_API_bill_info())

def parsing_json(json):
    pass



def request_pdf(pdf_url: str):
    response = requests.get(pdf_url)
    pdf_content = response.content
    print(type(pdf_content))

openAPI_url_config(os.getenv('OPENAPI_SEARCH_BILL_CODE'))
# request_pdf()

# ','5985B17F-6EB7-94FE-3648-67511E646665','1')

# function openBillFile(baseurl, bookid, type) {
# 	var url = baseurl+"?bookId="+escape(bookid)+"&type="+escape(type);
# 	$("#hiddenForm").attr("action", url);
# 	$("#hiddenForm").submit();
# }