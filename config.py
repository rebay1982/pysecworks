import os

class Config(object):
    DB_USERNAME = os.environ.get('DB_USERNAME') or 'secureworks'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'supersecret'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'canttouchthis'
