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

@app.route('/.well-known/acme-challenge/5mrqWpBvFNFRp231Ks33dkdext9fMKO3KIdoMHlGodQ')
def ssl_verify():
	return '5mrqWpBvFNFRp231Ks33dkdext9fMKO3KIdoMHlGodQ.8F7sdagzAk7DY5HKvzUL1xkmnY64VnXeQFRPzLJgzi8'

@app.errorhandler(404)
def not_found(e):
	return jsonify(error='invalid api key')
