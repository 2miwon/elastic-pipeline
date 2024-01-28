from typing import Union
from fastapi import FastAPI
import threading
from downstream.download import *
from downstream.raw_search import *
from database import *

app = FastAPI()

@app.get("/")
def read_all_bill_metadata():
    return read_all_bill_metadata()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}