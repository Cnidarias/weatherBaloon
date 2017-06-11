
from flask import Flask, request

import glob
import os
from flask import render_template


try:
    from parser import AprsFiParser
except ImportError as e:
    from .parser import AprsFiParser


def create_app(configfile=None):
    app = Flask(__name__)

    aprsparser = AprsFiParser(False)
    aprsparser.daemon = True
    aprsparser.start()
    return app

app = create_app()


@app.route('/', methods=['GET'])
def new_school():
    files = [os.path.basename(x) for x in glob.glob(os.path.join(app.static_folder, 'images', '*.jpg'))]
    print(files)
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
