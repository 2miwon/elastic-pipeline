from downstream.download import *
from fastapi import FastAPI

app = FastAPI()

@app.on_event('startup')
def load_data():
    loading_file()