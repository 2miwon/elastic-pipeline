import requests
import json
from bs4 import BeautifulSoup
# from config import *

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

def parse_search(byte_html: bytes):
    soup = BeautifulSoup(byte_html, 'html.parser')
    # results = [item for result in data['result'] for item in result['items']]
    count = soup.find("p", class_="sectionResult").find("span")
    chunk = soup.find(class_="sectionList")
    print(chunk)
    # data = [ 
    #     {
    #         "_title": li.a.text.strip(),
    #         "_href": li.a["href"],
    #         "_source": li.div.text.strip()
    #     } 
    #     for li in chunk.find_all("li")
    # ]
    # result = {
    #     "hits": {
    #         # "took": 3,
    #         "total": {
    #             "value": int(count.text.replace(',', '')),
    #             # "relation": "eq"
    #         },
    #         "hits": data
    #     }
    # }
    # for i in range(len(data)):
    #     result[i] = data[i]  
    data = [
        {
            "title": div[0][2:].strip(),
            "speaker": div2[0],
            "bill_no": div2[1],
            "date": div2[2]
        }
        for li in chunk.find_all("li")
        for div in [li.a.text.strip()[:-2].split(' [ ')]
        for div2 in [div[1].split(', ')]
    ] 
    result = {
        "total": int(count.text.replace(',', '')),
        "data": data
    } 
    return result

# {
#   "took" : 3,
#   "timed_out" : false,
#   "_shards" : {
#     "total" : 1,
#     "successful" : 1,
#     "skipped" : 0,
#     "failed" : 0
#   },
#   "hits" : {
#     "total" : {
#       "value" : 2,
#       "relation" : "eq"
#     },
#     "max_score" : 0.105360515,
#     "hits" : [
#       {
#         "_index" : "test",
#         "_type" : "_doc",
#         "_id" : "3",
#         "_score" : 0.105360515,
#         "_source" : {
#           "field" : "value three"
#         }
#       },
#       {
#         "_index" : "test",
#         "_type" : "_doc",
#         "_id" : "1",
#         "_score" : 0.105360515,
#         "_source" : {
#           "field" : "value two"
#         }
#       }
#     ]
#   }
# }

def get_search(query: str, page: str, sort: str) -> list:
    # return parse_search(raw_search(query))
    # return json.loads(raw_search(query))
    return json.dumps(parse_search(raw_search(query, page, sort)))

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