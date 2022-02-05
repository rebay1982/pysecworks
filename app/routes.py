from app import app
from flask import request
#from flask_login import current_user, login_user
from app.models import User

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/graphql')
def graphql():
    return "Hello, GraphQL!"

@app.route('/login', methods=['POST'])
def login():
    #if current_user.is_authenticated:
    #    return "Already Authenticated"

    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or password is None:
       return '400'

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return '403'

    # login_user(user, remember=True)
    return str(user)

#@app.route('/logout')
#def logout():
#    logout_user()
#    return "OK."

