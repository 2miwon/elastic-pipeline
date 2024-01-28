from flask import Flask, render_template
import threading
from downstream import loading_file
from metadata import *
from raw_search import *

def create_app():
    app = Flask(__name__)
    db_init_check()
    start_loading_file()

    @app.route('/')
    def onboarding():
        return read_all_bill_metadata()
    
    @app.route('/test')
    def test():
        # return render_template('test.html')
        return raw_search("sn")

    @app.route('/api')
    def fuck():
        pass

    return app

def start_loading_file():
    loading_thread = threading.Thread(target=loading_file)
    loading_thread.start() 
    print("Start loading_file in a separate thread")

if __name__ == '__main__':
    app = create_app()
    app.run(port=80)
    start_loading_file()