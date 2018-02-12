# encoding:utf-8
from . import cg
from app import db, app
from app.models import Post, Catagory
from operator import itemgetter
from flask import jsonify, request

@cg.route('/<item>')
def return_catagory_info(item):
    page = request.args.get('page', 1, type=int)
    pagination = Catagory.query.filter_by(item=item).order_by(Catagory.create_time.desc()).paginate(
        page, per_page=app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    item_list = pagination.items
    return jsonify(
        data=[each.post.return_dict() for each in item_list]
    )

@cg.route('/return_all_item')
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
    sorted_by_count_list = sorted(data, key=itemgetter('count'), reverse=True)
    return jsonify(
        data = sorted_by_count_list
    )

