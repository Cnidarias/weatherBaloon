
from flask import Flask, request

try:
    from frontend import frontend
    from parser import AprsFiParser
except ImportError as e:
    from .frontend import frontend
    from .parser import AprsFiParser


def create_app(configfile=None):
    app = Flask(__name__)
    app.register_blueprint(frontend)
    return app


app = create_app()

if __name__ == '__main__':

    aprsparser = AprsFiParser(False)
    aprsparser.daemon = True
    aprsparser.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
