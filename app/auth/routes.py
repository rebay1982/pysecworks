from app.auth import bp
from flask import request
from app.models import User

@bp.route('', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or password is None:
       return '400'

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return '403'

    return str(user)

