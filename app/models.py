import base64
import uuid
from datetime import datetime, timedelta
import os

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}:{}>'.format(self.username, self.password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):    # Expires in 1h.
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
   
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Lookup(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    response_code = db.Column(db.String)
    ip_address = db.Column(db.String, index=True, unique=True)

    def update(self, response_code):
        self.updated_at = datetime.utcnow()
        self.response_code = response_code
        db.session.add(self)

    @staticmethod
    def create_new(ip_address, response_code):
        now = datetime.utcnow()
        lookup = Lookup( \
            id = str(uuid.uuid4()), \
            created_at = now, \
            updated_at = now, \
            response_code = response_code, \
            ip_address = ip_address)
        db.session.add(lookup)
        return lookup










