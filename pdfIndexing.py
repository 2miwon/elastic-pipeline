import os
import base64
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch(
    "https://ysu-004.es.us-east-2.aws.elastic-cloud.com",
    basic_auth=('elastic', 'vvWYGFPKzPNbwZZBuTj3e4o8'),
)

folder_path = '/data/bills/'  # PDF 파일이 저장된 폴더 경로
bulk_actions = []  # Bulk 인덱싱을 위한 액션 리스트

count = 1
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        bill_number = filename.split('.')[0]  # 파일명에서 법안 번호 추출
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'rb') as file:
            encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
        
        # Bulk 인덱싱을 위한 액션 생성
        action = {
            "_index": "pdf_documents",
            "_op_type": "index",  # 문서 인덱싱 작업을 지정
            "_source": {
                "data": encoded_pdf,  # Ingest Pipeline에 의해 처리될 원본 데이터
                "bill_number": bill_number  # 법안 번호
            },
            "pipeline": "pdf_pipeline"  # 사용할 Ingest Pipeline 지정
        }
        bulk_actions.append(action)
        
        # 100개 문서마다 Bulk 인덱싱 실행
        if len(bulk_actions) >= 100:
            bulk(es, bulk_actions)
            bulk_actions = []  # 액션 리스트 초기화
            print(count)
            count += 1

# 남은 액션들에 대해 Bulk 인덱싱 실행
if bulk_actions:
    bulk(es, bulk_actions)

print(f"총 {len(bulk_actions)}개의 PDF 파일이 인덱싱되었습니다.")
