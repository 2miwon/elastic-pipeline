from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from downstream.download import *
from downstream.raw_search import *
from database import *

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

@app.get("/search/{query}")
def search(query: str):
    return get_search(query)

@app.get("/keword/{query}")
def keword(query: str):
    return get_keword(query)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.on_event('startup')
def init_data():
    loading_file()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_list_len, 'cron', second='*/5')
#     scheduler.start()