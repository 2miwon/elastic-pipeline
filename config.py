import os 
from dotenv import load_dotenv
load_dotenv(verbose=True)

#Asssembly API
ASSEMBLY_PDF_BASIC_URL = "https://likms.assembly.go.kr/filegate/servlet/FileGate"
OPENAPI_BASIC_URL = "https://open.assembly.go.kr/portal/openapi/"
ASSEMBLY_BILL_INFO_BASIC_URL = "https://likms.assembly.go.kr/bill/billDetail.do?"

OPENAPI_SEARCH_BILL_CODE = "TVBPMBILL11"

#Assembly System Web
BILL_DETAIL_CONTENTS_XPATH = "body > div > div:nth-child(3) > div:nth-child(3)"
BILL_ORIGIN_XPATH = "body > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(3) > div:nth-child(2) > table > tbody > tr > td:nth-child(4) > a:nth-child(2)"
BILL_ORIGIN_TABLE_XPATH = "tbody > tr > td:nth-child(4) > a:nth-child(2)"

RAW_SERACH_BILL_XPATH = "html > body > form > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)"


#SQLite3
DB_FILE_PATH = f'{os.getcwd()}/sqlite/database.db'