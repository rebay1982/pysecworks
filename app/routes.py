from app import app
from flask import request

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/graphql')
def graphql():
    return "Hello, GraphQL!"

@app.route('/login', methods=['POST'])
def login():
    return request.form.get('username') + ':' + \
        request.form.get('password')
