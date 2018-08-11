from app import app,db
from flask import jsonify
from app.models import BlogData
from restful import restful

@app.route('/')
@restful
def index():
    return "Hello World"

@app.route('/blog/like')
@restful
def increase_like():
    pre = BlogData.query.first()
    pre.like += 1
    db.session.commit()
    return {
        'like': pre.like
    }

@app.errorhandler(404)
def not_found(e):
    return jsonify(error='invalid api key')
