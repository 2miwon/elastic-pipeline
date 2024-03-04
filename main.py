from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from downstream.download import *
from downstream.search import *
from database import *
from pydantic import BaseModel

"""
fastAPI
"""

app = FastAPI()
# app.add_middleware(
#     # CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def read_all_bill_metadata():
    return read_all_bill_metadata()

class SearchRequest(BaseModel):
    query: str
    page: int
    sort: str

@app.post("/search/")
def search(request: SearchRequest):
    page = request.page or 1
    sort = request.sort or "RANK"
    return get_search(request.query, page, sort)

@app.get("/keword/{query}")
def keword(query: str):
    return get_keword(query)

@app.get("/file/{bill_id}")
def get_file(bill_id:int):
    return get_file(bill_id)

@app.on_event('startup')
def init_data():
    pass
    # loading_file()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_list_len, 'cron', second='*/5')
#     scheduler.start()