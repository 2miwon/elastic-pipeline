from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from downstream.download import *
from downstream.search import *
from database import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

"""
fastAPI
"""

app = FastAPI()

origins = [
    "http://allaw.site",
    "https://allaw.site",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return "server is OK"

class SearchRequest(BaseModel):
    query: str
    page: int = 1
    sort: str = "RANK"

@app.post("/search")
def search(request: SearchRequest):
    return get_search(request.query, request.page, request.sort)

@app.get("/keword/{query}")
def keword(query: str):
    return get_keword(query)

@app.get("/file/{bill_id}")
def get_file(bill_id:int):
        filepath = f'{os.getenv("BILL_PDF_LOCATION")}/{int(bill_id)}.pdf'
        return FileResponse(filepath, filename=f'{bill_id}.pdf', media_type='application/pdf')

@app.on_event('startup')
def init_data():
    pass
    # loading_file()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_list_len, 'cron', second='*/5')
#     scheduler.start()