import requests
import json

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

def parse_serach(byte_html: bytes):
    pass

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
    # 바이트 문자열을 문자열로 디코딩하고 JSON을 파싱
    json_string = byte_string.decode('utf-8').strip()
    data = json.loads(json_string)

    # Keyword 추출
    keywords = [item['keyword'] for result in data['result'] for item in result['items']]

    return keywords

def get_keword(query: str) -> list:
    return parse_keword(raw_keword(query))

print(get_keword("sns"))
print(type(raw_search("sns")))