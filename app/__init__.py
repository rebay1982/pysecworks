from flask import Flask
app = Flask(__name__) # The Flask instance, not the package.


# Here to avoid a circualar import with the routes module.
from app import routes
