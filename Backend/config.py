import os
basedir = os.path.abspath(os.path.dirname(__file__))

dbname = 'gas'
mongouri = 'mongodb://motieater:paska@ds145009.mlab.com:45009/gas'
allowed_extensions = {'log', 'json'}
secret_key = 'super secret key'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'praise-kek'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True