import requests
import json

def raw_search(query: str):
    url = 'https://likms.assembly.go.kr/nsrch/search.do'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': f'{1}',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PHAROSVISITOR=000017c1018d4d81bbff21b00ac93c0d; JSESSIONID=hHpVHKQP4UTVMEa77pIYv7et26Cw2uTxc6UZcOTttGE1rHmhn8vGkAgXgfBuZnvl.amV1c19kb21haW4vc2VhcmNoMQ==; _fwb=118I9cqxgr1lMv4GDW6W41A.1706262696919; _ga_8FY090CL6Y=GS1.1.1706262697.1.0.1706262700.0.0.0; _ga_LWN7D20CP3=GS1.1.1706399260.5.0.1706399260.0.0.0; _ga=GA1.3.1330563476.1706200401; _gid=GA1.3.1971371645.1706399261',
        'Host': 'likms.assembly.go.kr',
        'Origin': 'https://likms.assembly.go.kr',
        'Referer': 'https://likms.assembly.go.kr/nsrch/search.do',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'convert': 'fw',
        'target': 'common',
        'charset': 'utf-8',
        'query': query,
        'datatype': 'json',
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.request.body)
raw_search("sn")