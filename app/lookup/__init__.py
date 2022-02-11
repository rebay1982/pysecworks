from flask import Blueprint

bp = Blueprint('lookup', __name__)

from app.lookup import lookupqueue

