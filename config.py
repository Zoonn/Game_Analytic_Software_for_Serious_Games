import os
basedir = os.path.abspath(os.path.dirname(__file__))

secret_key = 'super secret key'

cwd = os.getcwd()

MONGODB_SETTINGS = {'DB': 'testing'}
CSRF_ENABLED = True

ALLOWED_EXTENSIONS = {'log', 'json'}
UPLOAD_FOLDER = basedir + '/app/JSONs'

AUTH_TYPE = 1
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'


