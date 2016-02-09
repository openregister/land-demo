#!/usr/bin/env python

import os
import glob
from openregister import Item
from openregister.representations.tsv import reader as tsv_reader
from openregister.stores.mongodb import MongoStore

mongo_host = os.getenv('DB_PORT_27017_TCP_ADDR', '127.0.0.1')
mongo_uri = 'mongodb://%s:27017/landregistry' % mongo_host

# load register register
store = MongoStore(mongo_uri, prefix="register_")

for filename in glob.glob('data/register/*.yaml'):
    item = Item()
    item.yaml = open(filename)
    store.add(item)


# load company register
store = MongoStore(mongo_uri, prefix="company_")

for item in tsv_reader(open('data/company/companies.tsv')):
    store.add(item)

store = MongoStore(mongo_uri, prefix="land_")
for item in tsv_reader(open('demodata/land/lands.tsv')):
    store.add(item)

store = MongoStore(mongo_uri, prefix="land_title_")
for item in tsv_reader(open('demodata/land-title/land-titles.tsv')):
    store.add(item)

store = MongoStore(mongo_uri, prefix="land_title_clause_")
for item in tsv_reader(open('demodata/land-title-clause/clauses.tsv')):
    store.add(item)

store = MongoStore(mongo_uri, prefix="land_deed_")
for item in tsv_reader(open('demodata/land-deed/land-deeds.tsv')):
    store.add(item)
