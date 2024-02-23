import os
import base64
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import *
import requests
import fitz  
from es_pdf_processing import extract_clean_text_from_pdf
from es_elasticsearch_utils import bulk_indexing, search_bill
from es_data_fetching import fetch_bill_data

last_processed_file = "last_processed.txt" # 마지막으로 처리된 파일명을 저장할 파일

# 마지막으로 처리된 파일명 또는 인덱스 번호를 읽어옵니다.
def read_last_processed():
    try:
        with open(last_processed_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# 마지막으로 처리된 파일명 또는 인덱스 번호를 저장합니다.
def write_last_processed(filename):
    with open(last_processed_file, "w") as file:
        file.write(filename)

# 법안 번호 목록을 파일로 저장합니다.
def save_bill_numbers(bill_numbers, filename="bill_numbers.txt"):
    with open(filename, "a") as file:
        for number in bill_numbers:
            file.write(f"{number}\n")


def indexing_pdf_file(file_id:str):
    folder_path = os.getenv('BILL_PDF_LOCATION')  # PDF 파일이 저장된 폴더 경로
    start_from = read_last_processed()
    started = False if start_from else True

    bulk_actions = []  # Bulk 인덱싱을 위한 액션 리스트
    bill_numbers = []  # 인덱싱할 법안 번호를 저장할 리스트

    for idx, filename in enumerate(sorted(os.listdir(folder_path))):
        if not started:
            if filename == start_from:
                started = True
            continue  # start_from까지 스킵
        if filename.endswith(".pdf"):
            bill_no = filename.split('.')[0]  # 파일명에서 법안 번호 추출
            bill_numbers.append(bill_no)  # 법안 번호를 리스트에 추가
            file_path = os.path.join(folder_path, filename)

            try:

                extracted_text = extract_clean_text_from_pdf(file_path)  
                # bill_data = fetch_bill_data(bill_no)
                # Bulk 인덱싱을 위한 액션 생성
                action = {
                    "_index": "pdf_documents",
                    "_op_type": "index",  # 문서 인덱싱 작업을 지정
                    "_id": bill_no,  # 문서 ID 명시적으로 지정
                    "_source": {
                        "bill_no": bill_no,
                        # "title": bill_data['BILL_NAME'],
                        # "speaker": bill_data['PROPOSER'],
                        # "date": bill_data['PROPOSE_DT'],
                        "content": extracted_text,  # 정제된 텍스트
                    }
                }
                bulk_actions.append(action)
                # print(action)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue


            # 100개 문서마다 Bulk 인덱싱 실행
            if len(bulk_actions) >= 50:
                print(idx + 1, "개의 PDF 파일을 인덱싱했습니다.")
                save_bill_numbers(bill_numbers, filename="bill_numbers.txt")
                bill_numbers = [] # 법안 번호 리스트 초기화
                write_last_processed(filename)  # 마지막으로 처리된 파일명 저장
                bulk_indexing(bulk_actions)
                bulk_actions = []  # 액션 리스트 초기화



    # 남은 액션들에 대해 Bulk 인덱싱 실행
    if bulk_actions:
        bulk_indexing(bulk_actions)

if __name__ == "__main__":
    # bills = search_bill("국회")
    # for bill in bills:
    #     #print dict bill data in formatted way
    #     print(f"법안번호: {bill['bill_no']}, 법안제목: {bill['title']}, 발의자: {bill['speaker']}, 발의일자: {bill['date']}, 내용: {bill['content']}")
    indexing_pdf_file("2119883")
    # print(read_pdf_file("2119883.pdf"))
    # print(f"총 {len(bulk_actions)}개의 PDF 파일이 인덱싱되었습니다.")
    
