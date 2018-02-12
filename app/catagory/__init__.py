#encoding:utf-8
from flask import Blueprint

cg = Blueprint('catagory', __name__)

from . import api
