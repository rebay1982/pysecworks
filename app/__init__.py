from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) # The Flask instance, not the package.
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Here to avoid a circualar import with the routes module.
from app import routes, models
