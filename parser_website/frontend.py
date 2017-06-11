import glob
import os
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)


@frontend.route('/', methods=['GET'])
def new_school():
    files = [os.path.basename(x) for x in glob.glob('static/images/*.jpg')]
    print(files)
    return render_template('index.html', files=files)

