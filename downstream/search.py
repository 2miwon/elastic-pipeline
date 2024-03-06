import requests
import json
from bs4 import BeautifulSoup
from config import *

def raw_search(query: str, page:int = 0, sort:str ="RANK", searchField:str = "ALL",startDate:str = '1970.01.01', endDate:str = '2024.02.04'):
    count = page * 10
    url = 'https://likms.assembly.go.kr/nsrch/search.do'
    data = {
        'startCount': count,
        'sort': sort, # RANK, DATE
        'collection': 'bill_all',
        'range': 'A',
        # 'startDate': startDate,
        # 'endDate': endDate,
        'searchField': searchField, #ALL,
        'reQuery': 2,
        'realQuery': query,
        'query': query,
    }
    response = requests.post(url, data=data)
    return response.content

def parse_search(data: dict):
    try:
        hits = data['hits']['hits']
        refine = [
            {
                "title": hit['_source']['title'],
                "speaker": hit['_source']['speaker'],
                "bill_no": hit['_source']['bill_no'],
                "date": hit['_source']['date'],
                # "contents": hit['_source']['content'],
            }
            for hit in hits
        ] 
        result = {
            "total": int(data['hits']['total']['value']),
            "result": refine
        } 
        return result
    except:
        return "No result"

def elastic_search(query: str, page: int, sort:str) -> list:
    url = f"{os.getenv('ELASTIC_ENDPOINT')}/pdf_documents/_search/"
    headers = {
        "Content-Type": "application/json"
    }
    # from_ = (int(page) - 1) * 10 if int(page) > 0 else 0
    from_ = int(page) * 10 if int(page) > 0 else 0
    data = {
        "_source": {
            "excludes": ["content"]
        },
        "query": {
            "match": {
                "content": query
            }
        },
        "size": 10,
        "from": from_
    }
    if sort == "DATE":
        data["sort"] = [{
            "bill_no": {
                "order": "desc"
            }
        }]
    auth = (os.getenv("ELASTIC_ID"), os.getenv("ELASTIC_PASSWORD"))

    response = requests.post(url, headers=headers, json=data, auth=auth)
    return response.json()

def get_search(query: str, page: int, sort: str) -> dict:

    # return parse_search(raw_search(query))
    # return json.loads(raw_search(query))
    # return json.dumps(parse_search(raw_search(query, page, sort)))
    return parse_search(elastic_search(query, page, sort))

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
    return ','.join(keywords)

def get_keword(query: str):
    # return parse_keword(raw_keword(query))
    return json.loads(raw_keword(query))

# if __name__ == "__main__":
#     print(get_search("국회"))