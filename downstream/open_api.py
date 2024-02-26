import copy
import os
import requests
from config import *

basic_param = {
    "KEY": os.getenv('ASSEMBLY_OPENAPI_KEY'),
    "Type": "json"
}

def openAPI_url_config(code: str, parameter: dict) -> str:
    """
    openAPI 요청 url 구성
    """
    url = OPENAPI_BASIC_URL + code + '?'
    for param, value in parameter.items():
        url += param + '=' + value + '&'
    return url


def get_bill_api_data(pIndex: int) -> dict:
    param = copy.deepcopy(basic_param)
    # param["BILL_NO"] = str(bill_no)
    param['pIndex'] = str(pIndex)
    param['pSize'] = "1"
    response = requests.get(openAPI_url_config(OPENAPI_SEARCH_BILL_CODE ,param))
    if response.status_code == 200:
        if OPENAPI_SEARCH_BILL_CODE not in response.json():
            return None
        
        content_json = response.json()[OPENAPI_SEARCH_BILL_CODE]
        return parsing_json(content_json)
    else:
        raise Exception("Fail to request API")
    
def parsing_json(json: dict) -> dict:
    if json[0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
        body = json[1]['row']
        return {
            'BILL_NO': body[0]['BILL_NO'],
            'BILL_ID': body[0]['BILL_ID'],
            'BILL_NAME': body[0]['BILL_NAME'],
            'PROPOSER': body[0]['PROPOSER'],
            'PROPOSE_DT': body[0]['PROPOSE_DT'],
        }
    else:
        return None