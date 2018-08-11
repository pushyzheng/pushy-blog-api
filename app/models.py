#encoding:utf-8
from app import db,app
import bleach,re,time
from datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import qrcode
from app import picSet

class Admin(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(32),index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def varify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_access_token(self,expiration = 3600): #设置access_token的默认过期时间为一小时
        s = Serializer(app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id})

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer,primary_key=True)
    post_url = db.Column(db.String(100))
    title = db.Column(db.Text)
    cover_url = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now)
    good = db.Column(db.Integer,default=1)
    comments = db.relationship('Comment',backref='post')
    catagory = db.relationship('Catagory',backref='post')

    def return_dict(self):
        return {
            'title':self.title,
            'body':self.body,
            'content':self.body_html,
            'post_id':self.post_id,
            'cover_url':self.cover_url,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M:%S')[:-9],
            'catagory':[each.item for each in self.catagory],
            'post_url':self.post_url
        }

    @staticmethod
    def create_url_qrcode(self, value, oldvalue, initiator):
        path = '/static/pics/{}_qrcode.jpg'.format(str(value))
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        post_site_url = 'https://pushy.site/posts/' + str(value)
        qr.add_data(post_site_url)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(path)
        self.post_url = 'https://static.pushy.site/pics/{}_qrcode.jpg'.format(str(value))

class Catagory(db.Model):
    __tablename__ = 'catagory'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    item = db.Column(db.String(20))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.post_id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def return_dict(self):
        return {
        	'id':self.id,
            'title':self.title,
            'body':self.body,
            'content':self.body_html,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M:%S')[:-9],
        }

    @staticmethod
    def change_markdown_to_html(self, value, oldvalue, initiator):
        #允许存在的标签：
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p','img']
        #标签允许的参数：
        attrs = {
            'img': ['src'],
            '*':['class'],
            'a':['href']
        }
        self.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html',extensions=['markdown.extensions.extra']),
                         tags=allowed_tags,
                         strip=True,attributes=attrs)
        )
        self.body_html = re.sub('<a','<a target="_blank"',self.body_html)
        self.body_html = re.sub('<pre><code>', '<pre style="font-size:15px;cursor:text;background-color:#F7F7F7;"><code class="language-python">', self.body_html)
        self.body_html = re.sub('<pre><code class="', '<pre class=" language-python" style="font-size:15px;cursor:text;background-color:#F7F7F7"><code class=" language-', self.body_html)
        self.body_html = re.sub('<img src="pic/','<img class="mdui-img-fluid" src="http://static.pushy.site/pics/',self.body_html)

db.event.listen(Code.body,'set',Code.change_markdown_to_html)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    @staticmethod
    def change_markdown_to_html(self, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        attrs = {
            '*': ['class'],
            'img': ['src', 'alt'],
            'a': ['href']
        }
        self.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True, attributes=attrs)
        )
        self.body_html = re.sub('<img', '<img class="img-fluid"', self.body_html)

db.event.listen(Comment.body, 'set', Comment.change_markdown_to_html)

class BlogData(db.Model):
    __tablename__ = 'blog_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    like = db.Column(db.Integer)
