# -*- coding: utf-8 -*-
import os

class Config(object):
    SETTINGS = os.environ.get('SETTINGS')
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PREMISES_REGISTER = os.environ.get('PREMISES_REGISTER')
    MONGO_URI = os.environ.get('MONGO_URI')
    PRODUCTS_OF_ANIMAL_ORIGIN_PREMISES = os.environ.get('PRODUCTS_OF_ANIMAL_ORIGIN_PREMISES')
    PRODUCTS_OF_ANIMAL_ORIGIN_SECTION = os.environ.get('PRODUCTS_OF_ANIMAL_ORIGIN_SECTION')
    PRODUCTS_OF_ANIMAL_ORIGIN_ACTIVITY = os.environ.get('PRODUCTS_OF_ANIMAL_ORIGIN_ACTIVITY')


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-dev-not-secret')

class TestConfig(Config):
    TESTING = True
