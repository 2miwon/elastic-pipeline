from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import threading
from downstream.download import *
from downstream.search import *
from database import *

"""
for Flask
"""

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def onboarding():
        return "server is OK"
    
    @app.route('/test')
    def test():
        return elastic_search("sns")
    
    @app.route('/debug/<query>')
    def debug(query):
        return elastic_search(query, page=0, sort="RANK")

    @app.get("/search/<query>")
    def search(query: str):
        page = request.args.get('page', 0)
        sort = request.args.get('sort', "RANK")
        return get_search(query, page=int(page), sort=sort)

    @app.get("/keword/<query>")
    def keword(query: str):
        return get_keword(query)

    @app.get('/file/<bill_id>')
    def get_file(bill_id:int):
        filepath = f'/data/bills/{int(bill_id)}.pdf'
        return send_file(filepath, as_attachment=True)
    
    return app

def start_loading_file():
    loading_thread = threading.Thread(target=loading_file)
    loading_thread.start() 

    # print("Start loading_file in a separate thread")

if __name__ == '__main__':
    app = create_app()
    app.run(port=80)
    # start_loading_file()
