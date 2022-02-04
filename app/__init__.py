from flask import Flask
from config import Config
app = Flask(__name__) # The Flask instance, not the package.
app.config.from_object(Config)

# Here to avoid a circualar import with the routes module.
from app import routes
