#encoding:utf-8
from app import app,db
from . import code
from flask import jsonify,request,render_template
from app.models import Code
import requests
import json

@code.route('/')
def return_code_pagination():
    page = request.args.get('page', 1, type=int)
    pagination = Code.query.order_by(Code.create_time.desc()).paginate(
        page, per_page=app.config['FLASKY_CODE_PER_PAGE'],
        error_out=False
    )
    code_list = pagination.items
    return jsonify(
        error_code=0,
        error_msg='',
        data=[each.return_dict() for each in code_list]
    )

@code.route('/create',methods=['POST','GET'])
def create_one_code():
    if request.method =='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not (title and content):
            return jsonify(
                error_code=1,
                error_msg='No complete form data.',
                data=''
            )
        new_code = Code(title=title,body=content)
        db.session.add(new_code)
        db.session.commit()
        return render_template('code.html',code=new_code)
    else:
        return jsonify(
            error='Method Not Allowed.'
        )

