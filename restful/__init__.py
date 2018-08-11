# encoding:utf-8
from functools import wraps
from flask import Flask, jsonify
import copy
import http

# 定义返回字段
response_template = {
    'data': '',
    'error_code': 0,
    'error_msg': ''
}

def restful(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            resp = copy.copy(response_template)
            resp['error_code'] = 0
            resp['data'] = data
            return jsonify(resp)
        except UnauthorizedError as e:
            resp = copy.copy(response_template)
            resp['error_code'] = 1
            resp['error_msg'] = e.args[0]
            return jsonify(resp),http.HTTPStatus.UNAUTHORIZED
        except BadRequestError as e:
            resp = copy.copy(response_template)
            resp['error_code'] = 1
            resp['error_msg'] = e.args[0]
            return jsonify(resp),http.HTTPStatus.BAD_REQUEST
        except NotFoundError as e:
            resp = copy.copy(response_template)
            resp['error_code'] = 1
            resp['error_msg'] = e.args[0]
            return jsonify(resp), http.HTTPStatus.NOT_FOUND
        except RestfulException as e:
            resp = copy.copy(response_template)
            code = e.args[1]
            resp['error_code'] = 1
            resp['error_msg'] = e.args[0]
            return jsonify(resp),code
    return wrapper

from .exception import *