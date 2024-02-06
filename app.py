from flask import Flask, render_template, request
import threading
from downstream.download import *
from downstream.raw_search import *
from database import *

"""
for Flask
"""

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def onboarding():
        return "server is OK"
    
    @app.route('/test')
    def test():
        # return render_template('test.html')
        return get_keword("sns")

    @app.get("/search/<query>")
    def search(query: str):
        page = request.args.get('page', 0)
        sort = request.args.get('sort', "RANK")
        return get_search(query, page=int(page), sort=sort)

    @app.get("/keword/<query>")
    def keword(query: str):
        return get_keword(query)

    return app

def start_loading_file():
    loading_thread = threading.Thread(target=loading_file)
    loading_thread.start() 

    # print("Start loading_file in a separate thread")

if __name__ == '__main__':
    app = create_app()
    app.run(port=80)
    # start_loading_file()
