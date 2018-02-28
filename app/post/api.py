# encoding:utf-8
import time, hashlib
from datetime import datetime
from flask import jsonify, request,render_template
from . import post
from app.models import Post, Catagory
from app import db, app, picSet

@post.route('/')
def return_page_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page, per_page=app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return jsonify(
        error_code=0,
        error_msg='',
        data=[each.return_dict() for each in posts]
    )

@post.route('/<post_id>', methods=['GET', 'DELETE'])
def return_one_post(post_id):
    """
    由post_id返回具体文章的内容
    """
    if request.method == 'GET':
        post = Post.query.filter_by(post_id=post_id).first()
        return jsonify(
            data=post.return_dict()
        )
    elif request.method == 'DELETE':
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return jsonify(
                error_code=1,
                error_msg='no this post',
                data=""
            )
        # 删除文章对应的标签：
        all_catagory_list = Catagory.query.filter_by(post_id=post_id).all()
        for each in all_catagory_list:
            db.session.delete(each)
        db.session.delete(post)
        db.session.commit()
        return jsonify(
            error_code=0,
            error_msg='',
            data=""
        )


@post.route('/return_all_posts')
def return_all_posts():
    all_posts_list = Post.query.order_by(Post.create_time.desc()).all()
    return jsonify(
        data=[each.return_dict() for each in all_posts_list]
    )


@post.route('/write', methods=['POST', 'GET'])
def write_post_api():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        catagory = request.form.get('catagory')
        file = request.files.get('file')
        if not (title and content and catagory and file):
            return jsonify(
                error_code=1,
                error_msg='No complete form data.',
                data=''
            )
        post_id = int(time.time())
        filename = picSet.save(file, name='cover-{}'.format(post_id) + '.')
        cover_url = 'https://static.pushy.site/pics/{}'.format(filename)
        new_post = Post(title=title, body=content, post_id=post_id, cover_url=cover_url)
        db.session.add(new_post)
        db.session.commit()
        # 将文章的标签存入Catagory模型的item字段中：
        for each in catagory.split(','):
            new_item = Catagory(item=each, post_id=post_id)
            db.session.add(new_item)
        db.session.commit()
        return jsonify(
            error_code=0,
            error_msg='',
            data=new_post.return_dict()
        )
    else:
        return jsonify(
            error='Method Not Allowed.'
        )

@post.route('/update', methods=['POST', 'GET'])
def update_post_api():
    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')
        post_id = request.json.get('post_id')
        if not (title and content and post_id):
            return jsonify(
                error_code=1,
                error_msg='No complete form data.',
                data=''
            )
        update_time = datetime.now()
        post = Post.query.filter_by(post_id=post_id).first()
        post.title = title
        post.body = content
        post.update_time = update_time
        db.session.commit()
        return jsonify(
            error_code=0,
            error_msg='',
            data = post.return_dict()
        )
    else:
        return jsonify(
            error='Method Not Allowed.'
        )


@post.route('/write/pic', methods=['POST', 'GET'])
def upload_post_picture():
    if request.method == 'POST':
        for form_file in request.files.getlist('file'):
            picSet.save(form_file)
            url = 'http://static.pushy.site/pic/' + form_file.filename
            return jsonify(
                error_code=0,
                error_msg='',
                data=url
            )

@post.route('/like', methods=['POST', 'GET'])
def increase_post_like():
    if request.method == 'POST':
        post_id = request.json.get('post_id')
        pre = Post.query.filter_by(post_id=post_id).first()
        if not pre.good:
            pre.good = 1
        else:
            pre.good += 1
        db.session.commit()
        return jsonify(
            data={
                'good': pre.good
            }
        )
