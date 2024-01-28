import requests
import json
from bs4 import BeautifulSoup

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

def parse_search(byte_html: bytes):
    soup = BeautifulSoup(byte_html, 'html.parser')
    print(soup)
    # results = [item for result in data['result'] for item in result['items']]

    # return results

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
