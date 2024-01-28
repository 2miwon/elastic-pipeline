import requests
import json
from bs4 import BeautifulSoup
from config import *

def raw_search(query: str):
    url = 'https://likms.assembly.go.kr/nsrch/search.do'
    data = {
        'convert': 'fw',
        'target': 'common',
        'charset': 'utf-8',
        'query': query,
        'datatype': 'json',
    }

    response = requests.post(url, data=data)
    return response.content

# /html/body/form/div/div[2]/div[2]/div[2]/div[1]
def parse_search(byte_html: bytes):
    soup = BeautifulSoup(byte_html, 'html.parser')
    # results = [item for result in data['result'] for item in result['items']]
    chunk = soup.select_one(RAW_SERACH_BILL_XPATH)
    results = [ 
        {
            "href": li.a["href"],
            "text": li.a.text.strip()
        } 
        for li in chunk.find_all("li")
    ]
    return results

def raw_keword(query: str):
    url = 'https://likms.assembly.go.kr/nsrch/ark/ark_trans.do'
    data = {
        'convert': 'fw',
        'target': 'common',
        'charset': 'utf-8',
        'query': query,
        'datatype': 'json',
    }
    response = requests.post(url, data=data)
    return response.content

def parse_keword(byte_string: bytes):
    json_string = byte_string.decode('utf-8').strip()
    data = json.loads(json_string)
    keywords = [item['keyword'] for result in data['result'] if result['totalcount'] for item in result['items']]
    return keywords

def get_keword(query: str) -> list:
    return parse_keword(raw_keword(query))

def get_search(query: str) -> list:
    return parse_search(raw_search(query))

print(get_search('sn'))
