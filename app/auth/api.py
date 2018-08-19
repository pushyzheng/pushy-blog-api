#encoding:utf-8
from . import auth
from app.models import Admin
from flask import request
from restful import *

@auth.route('/login', methods=['POST'])
@restful
def admin():
    username = request.json.get('username')
    password = request.json.get('password')
    if not (username and password):
        raise BadRequestError("The request body is not present")
    admin = Admin.query.filter_by(username=username).first()
    if admin is not None and admin.varify_password(password):
        token = admin.generate_access_token()
        return {
            'access_token':token.decode('utf-8')
        }
    else:
        raise UnauthorizedError("Invalid password or no this user")