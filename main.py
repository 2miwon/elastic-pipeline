from typing import Union
from fastapi import FastAPI
import threading
from downstream.download import *
from downstream.raw_search import *
from database import *

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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.on_event('startup')
def init_data():
    print("hello!")
    db_init_check()
    loading_file()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_list_len, 'cron', second='*/5')
#     scheduler.start()