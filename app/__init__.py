#encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_cors import CORS
from flask_uploads import UploadSet,IMAGES,configure_uploads

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
CORS(app)
picSet = UploadSet('picSet',IMAGES)
configure_uploads(app,picSet)

from .post import post as post_blueprint
app.register_blueprint(post_blueprint, url_prefix='/posts')

from .catagory import cg as catagory_blueprint
app.register_blueprint(catagory_blueprint,url_prefix='/catagory')

from .code import code as code_blueprint
app.register_blueprint(code_blueprint,url_prefix='/code')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint,url_prefix='/auth')

from app import views,models