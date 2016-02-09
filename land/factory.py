# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from pymongo import MongoClient


def asset_path_context_processor():
    return {'asset_path': '/static/'}

def category_filter(s):
    section = s.split(' ')[0]
    activity = s.split(' ')[1]
    return "%s %s" % (section, activity)

def create_app(config_filename):
    ''' An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    '''
    app = Flask(__name__)
    app.config.from_object(config_filename)
    register_errorhandlers(app)
    register_blueprints(app)
    app.context_processor(asset_path_context_processor)
    app.jinja_env.filters['category_filter'] = category_filter
    register_db(app)
    return app

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_blueprints(app):
    from land.frontend.views import frontend
    app.register_blueprint(frontend)

# def register_extensions(app):
#     pass


def register_db(app):
    if app.config['SETTINGS'] == 'config.DevelopmentConfig':
        db = MongoClient(app.config['MONGO_URI'])['lookup']
    else:
        db = MongoClient(app.config['MONGO_URI']).get_default_database()
    app.db = db
