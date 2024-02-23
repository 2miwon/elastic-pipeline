# main.py
from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from typing import Optional
import os
from config import *

app = FastAPI()

# Elasticsearch 클라이언트 인스턴스 생성
es = Elasticsearch(
    hosts = [os.getenv('ELASTIC_LOCAL_ENDPOINT')],
    basic_auth=(os.getenv('ELASTIC_LOCAL_ID'), os.getenv('ELASTIC_LOCAL_PASSWORD')),
    ca_certs = os.getenv('ELASTIC_LOCAL_CERT')
)

@app.get("/search/{query}")
async def search(query: str, page: Optional[int] = 1, sort: Optional[str] = "RANK"):
    # Elasticsearch에서 검색 질의 구성
    body = {
        "query": {
            "match": {
                "content": query
            }
        },
        "from": (page - 1) * 10,  # 페이지네이션 구현
        "size": 10
    }

    if sort == "DATE":
        body["sort"] = [{"date": {"order": "desc"}}]  # 최신순 정렬

    # Elasticsearch 검색 실행
    try:
        response = es.search(index="pdf_documents", body=body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 검색 결과 반환
    return {
        "total": response["hits"]["total"]["value"],
        "results": [hit["_source"] for hit in response["hits"]["hits"]]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
