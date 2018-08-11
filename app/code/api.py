#encoding:utf-8
from app import app,db
from . import code
from flask import request,render_template
from app.models import Code
from restful import *

@code.route('/')

def return_code_pagination():
    page = request.args.get('page', 1, type=int)
    pagination = Code.query.order_by(Code.create_time.desc()).paginate(
        page, per_page=app.config['FLASKY_CODE_PER_PAGE'],
        error_out=False
    )
    code_list = pagination.items
    return [each.return_dict() for each in code_list]

@code.route('/create',methods=['POST'])
@restful
def create_one_code():
    title = request.form.get('title')
    content = request.form.get('content')
    if not (title and content):
        raise BadRequestError("The request body is not present")
    new_code = Code(title=title,body=content)
    db.session.add(new_code)
    db.session.commit()
    return render_template('code.html',code=new_code)

