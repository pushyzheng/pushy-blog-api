#encoding:utf-8
from . import auth
from app.models import Admin
from flask import request,jsonify

@auth.route('/login',methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if not (username and password):
            return jsonify(
                error_code=1,
                error_msg='No complete form data.',
                data=""
            )
        admin = Admin.query.filter_by(username=username).first()
        if admin is not None and admin.varify_password(password):
            token = admin.generate_access_token()
            return jsonify(
                error_code=0,
                error_msg='',
                data={
                    'access_token':token.decode('utf-8')
                }
            )
        else:
            return jsonify(
                error_code=1,
                error_msg='Invalid password or no this user',
                data=""
            )

    else:
        return jsonify(
            error='Method Not Allowed.'
        )