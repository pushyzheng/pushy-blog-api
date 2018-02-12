#encoding:utf-8
from flask import Blueprint

code = Blueprint('code', __name__)

from . import api
