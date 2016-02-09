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

import os
import requests
from openregister import Item
from openregister.stores.mongodb import MongoStore

mongo_host = os.getenv('DB_PORT_27017_TCP_ADDR', '127.0.0.1')
mongo_uri = 'mongodb://%s:27017/landregistry' % mongo_host

land_title_store = MongoStore(mongo_uri, prefix="land_title_")
land_title_clause_store = MongoStore(mongo_uri, prefix="land_title_clause_")


from land.frontend.forms import SearchForm

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@frontend.route('/land/title/<number>', methods=['GET'])
def register_view(number):
    meta, land_title = land_title_store.find(query={'land-title': number})
    meta, clauses = land_title_clause_store.find(query={'land-title': number})
    return render_template('register_view.html', land_title=land_title[0], clauses=clauses)
