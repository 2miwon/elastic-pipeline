from flask import Flask
import threading
from downstream import loading_file
from metadata import *

def create_app():
    app = Flask(__name__)
    db_init_check()
    start_loading_file()

    @app.route('/')
    def onboarding():
        return read_all_bill_metadata()
    
    return app

def start_loading_file():
    # Start loading_file in a separate thread
    print("Start loading_file in a separate thread")
    loading_thread = threading.Thread(target=loading_file)
    loading_thread.start() 

if __name__ == '__main__':
    app = create_app()
    app.run(port=80)
    start_loading_file()
