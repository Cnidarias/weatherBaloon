
from flask import Flask, request

import glob
import os
from flask import render_template
from queue import Queue
import json


try:
    from parser import AprsFiParser
except ImportError as e:
    from .parser import AprsFiParser

aprs_data = Queue()

def create_app(configfile=None):
    app = Flask(__name__)

    aprsparser = AprsFiParser(False, aprs_data, app.logger)
    aprsparser.daemon = True
    aprsparser.start()
    return app

app= create_app()


@app.route('/', methods=['GET'])
def new_school():
    files = [os.path.basename(x) for x in glob.glob(os.path.join(app.static_folder, 'images', '*.jpg'))]
    print(files)
    return render_template('index.html', files=files)


@app.route('/data', methods=['POST'])
def post_data():
    aprs_data.put(request.get_json()['data'])
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
