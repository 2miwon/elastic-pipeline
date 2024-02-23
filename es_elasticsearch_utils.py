from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import *
import os

es = Elasticsearch(
    hosts = [os.getenv('ELASTIC_LOCAL_ENDPOINT')],
    basic_auth=(os.getenv('ELASTIC_LOCAL_ID'), os.getenv('ELASTIC_LOCAL_PASSWORD')),
    ca_certs = os.getenv('ELASTIC_LOCAL_CERT')
)



def bulk_indexing(bulk_actions):
    bulk(es, bulk_actions)

def search_bill(content: str):
    query = {
        "query": {
            "match": {
                "content": content
            }
        }
    }
    response = es.search(index="pdf_documents", body=query)
    bills = []
    
    for hit in response['hits']['hits']:
        bill_number = hit['_source']['bill_no']
        title = hit['_source']['title']
        speaker = hit['_source']['speaker']
        date = hit['_source']['date']
        doc_content = hit['_source']['content'][:10] # 내용의 앞부분 10자

        bill = {
            "bill_no": bill_number,
            "title": title,
            "speaker": speaker,
            "date": date,
            "content": doc_content
        }
        bills.append(bill)        
    return bills

# if __name__ == "__main__":
#     print(es.info())
#     print(search_bill("국회")[0])