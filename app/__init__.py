import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_login import LoginManager


app = Flask(__name__) # The Flask instance, not the package.
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#login = LoginManager(app)

# Here to avoid a circualar import with the routes module.
from app import routes, models, errors

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Make these configurable
    file_handler = RotatingFileHandler('logs/pysecworks.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter( \
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("PySecWorks Startup.")
