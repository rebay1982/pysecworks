import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DB_USERNAME = os.environ.get('DB_USERNAME') or 'secureworks'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'supersecret'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'canttouchthis'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

