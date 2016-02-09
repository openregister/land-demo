#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests

from flask.ext.script import Shell, Server, Manager
from pymongo import MongoClient

from land import app

app.debug = True
port = os.environ.get('PORT', 8000)

manager = Manager(app)
manager.add_command('server', Server(host="0.0.0.0", port=port))


@manager.command
def load_local_data():
    import time
    premises_register = app.config['PREMISES_REGISTER']
    entries_url = '%s/entries.json' % premises_register
    page = 1

    if app.config['SETTINGS'] == 'config.DevelopmentConfig':
        db = MongoClient(app.config['MONGO_URI'])['lookup']
    else:
        db = MongoClient(app.config['MONGO_URI']).get_default_database()

    premises = db.premises
    while True:
        params = {'pageIndex': page, 'pageSize': 1000}
        res = requests.get(entries_url, params)
        if res.json():
            for count, p in enumerate(res.json()):
                if p['entry']['company']:
                    attach_fsa_data(p)
                    premises.insert(p)
                    if count % 10 == 0:
                        time.sleep(5)
            page += 1
        else:
            break


def attach_fsa_data(premises):
    premises_url = app.config['PRODUCTS_OF_ANIMAL_ORIGIN_PREMISES']+'/search'
    headers = {'Content-type': 'application/json'}
    params = {'_representation': 'json', '_query': premises['entry']['premises']}
    section_url = app.config['PRODUCTS_OF_ANIMAL_ORIGIN_SECTION']+'/products-of-animal-origin-section/'
    activity_url = app.config['PRODUCTS_OF_ANIMAL_ORIGIN_ACTIVITY']+'/products-of-animal-origin-activity/'

    resp = requests.get(premises_url, headers=headers, params=params)
    if resp.status_code == 200:
        activities = resp.json()['entries'][0]['entry']['food-establishment-categories']
        licences = []
        for activity in activities:
            sect, act = activity.split(':')
            sect_url = section_url + sect
            act_url = activity_url + act
            resp = requests.get(act_url, params={'_representation': 'json'})
            activity_name = resp.json()['entry']['name']
            resp = requests.get(sect_url, params={'_representation': 'json'})
            section_name = resp.json()['entry']['name']
            licences.append("%s (%s %s)" % (activity, section_name, activity_name))
    premises['licences'] = licences


if __name__ == '__main__':
    manager.run()
