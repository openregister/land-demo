from flask import (
    Blueprint,
    render_template,
    flash,
    request,
    abort,
    current_app,
    redirect,
    url_for
)

import requests

from land.frontend.forms import SearchForm

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/', methods=['GET'])
def index():
    return render_template('index.html')
