# encoding:utf-8
from . import cg
from app import app, db
from app.models import Catagory, Tag
from operator import itemgetter
from flask import request
from restful import *

@cg.route('/tags')
@restful
def return_all_category():
    return [item.return_dict() for item in Tag.query.all()]


@cg.route('/tags', methods=['POST'])
@restful
def add_tag():
    name = request.json['name']
    if not name:
        raise BadRequestError("The request body is not present")
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return tag.return_dict()

@cg.route('/<item>')
@restful
def return_catagory_info(item):
    page = request.args.get('page', 1, type=int)
    pagination = Catagory.query.filter_by(item=item).order_by(Catagory.create_time.desc()).paginate(
        page, per_page=app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    item_list = pagination.items
    return [each.post.return_dict() for each in item_list]

@cg.route('/items')
@restful
def return_all_no_repeat_item():
    all_item_list = [each.item for each in Catagory.query.all()]
    # 通过转换为集合再转换为列表去重：
    all_item_np_list = list(set(all_item_list))
    data = []
    for each in all_item_np_list:
        dict = {}
        dict['item'] = each
        dict['count'] = all_item_list.count(each)
        data.append(dict)
    # 对标签的个数通过sorted方法更具count键进行降序操作：
    return sorted(data, key=itemgetter('count'), reverse=True)

