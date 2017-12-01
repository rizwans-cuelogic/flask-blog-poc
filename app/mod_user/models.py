import datetime

from app import db,lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import Enum



class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True)
	email = db.Column(db.String(120),index=True,unique=True)
	contact = db.Column(db.String(12),nullable=True)
	Address = db.Column(db.String(540),nullable=True)
	Gender = db.Column(db.String(10),nullable=True)
	password_hash = db.Column(db.String(128))
	blogs = db.relationship('Blog', backref='author',cascade="all,delete",lazy='dynamic')
	user_comments =db.relationship('Comment', backref='commentator',cascade="all,delete",lazy='dynamic')

	def __str__(self):
		return '<USER %s>' %(self.username)

	@property
	def password(self):
		raise AttributeError("Password is not readable attribute")

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def avatar(self,size):
		return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Blog(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(140),nullable=False)
	content = db.Column(db.String,nullable=False)
	publication_date = db.Column(db.DateTime,default=datetime.datetime.utcnow)
	published = db.Column(db.Boolean)
	user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
	comments = db.relationship('Comment',backref='blog',cascade="all,delete",lazy='dynamic')

	def __str__(self):
		return '<Blog %s>' %(self.content)

class Comment(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.String(),nullable=False)
	created = db.Column(db.DateTime,default=datetime.datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'))
	parent = db.Column(db.Integer,db.ForeignKey('comment.id'),nullable=True)
	cm_replies = db.relationship('Comment',remote_side=[id],backref='replies',cascade="all,delete",lazy="joined")
