from app import app,db
from flask import jsonify,request,redirect
from app.models import BlogData,Post


@app.route('/')
def index():
    return jsonify(data="")


@app.route('/blog/like')
def increase_like():
    pre = BlogData.query.first()
    pre.like += 1
    db.session.commit()
    return jsonify(
        data={
            'like':pre.like
        }
    )

@app.errorhandler(404)
def not_found(e):
    return jsonify(error='invalid api key')
