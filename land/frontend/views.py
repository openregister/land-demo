from flask import (
    Blueprint,
    render_template,
    flash,
    logging,
    request,
    abort,
    current_app,
    redirect,
    url_for
)

import os
import re
import requests
from openregister.client import Client
from openregister.stores.mongodb import MongoStore

mongo_host = os.getenv('DB_PORT_27017_TCP_ADDR', '127.0.0.1')
mongo_uri = 'mongodb://%s:27017/landregistry' % mongo_host

land_title_store = MongoStore(mongo_uri, prefix="land_title_")
land_title_clause_store = MongoStore(mongo_uri, prefix="land_title_clause_")
company_store = MongoStore(mongo_uri, prefix="company_")

client = Client()

from land.frontend.forms import SearchForm

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@frontend.route('/land/title/<number>', methods=['GET'])
def register_view(number):

    meta, land_titles = land_title_store.find(query={'land-title': number})
    land_title = land_titles[0]

    meta, clauses = land_title_clause_store.find(query={'land-title': number})

    section_order = ['PROPERTY', 'PROPRIETORSHIP', 'CHARGES']
    sections = {
        'PROPERTY': {
            'name': 'A',
            'title': 'Property',
            'clauses': [],
            'intro': 'This section describes the land and estate comprised in the title.'
        },
        'PROPRIETORSHIP': {
            'name': 'B',
            'title': 'Proprietorship',
            'clauses': [],
            'intro': 'This section specifies the class of title and identifies the owner. It contains any entries that affect the right of disposal.'
        },
        'CHARGES': {
            'name': 'C',
            'title': 'Charges',
            'clauses': [],
            'intro': 'This section contains any charges and other matters that affect the land.'
        }
    }

    records = {}

    address = client.item('address', land_title['address'])
    records['address:' + address.address] = address.json

    company_re = re.compile('\[\[company:([0-9]*)\]\]')

    for clause in clauses:
        clause['text'] = clause['text'].strip()
        sections[clause['land-title-section']]['clauses'].append(clause)
        for number in company_re.findall(clause['text']):
            meta, company = company_store.find(query={'company': number})
            records['company:'+number] = company[0].json

    return render_template('register_view.html', address=address, land_title=land_title, sections=sections, section_order=section_order, records=records)
