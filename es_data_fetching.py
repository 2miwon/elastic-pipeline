import requests

def fetch_bill_data(idx):
    url = f"https://open.assembly.go.kr/portal/openapi/TVBPMBILL11?KEY=f98b6728741e4d03a071d37d0319c69b&BILL_NO={idx}&TYPE=JSON"
    response = requests.get(url)
    data = response.json()['TVBPMBILL11'][1]['row'][0]
    return data

def search(query: str, page: int, sort: str):
    url = f"http://localhost:8000/search/{query}?page={page}&sort={sort}"
    response = requests.get(url)
    data = response.json()
    return data
if __name__ == "__main__":
    # print(fetch_bill_data("2001048"))
    print(search("국회", 1, "RANK")["results"][0])