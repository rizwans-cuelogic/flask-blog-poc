import unittest
import factory
import config
from flask import Flask,url_for,session
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog,Comment
from ..mod_blog.forms import CommentForm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import orm
from sqlalchemy import Column, Integer, Unicode, create_engine

engine = create_engine(config.TestingConfig.SQLALCHEMY_DATABASE_URI)
Session = orm.scoped_session(orm.sessionmaker(bind=engine))


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = User
		sqlalchemy_session = Session   # the SQLAlchemy session object

	username = "test"
	email = "test@test.com"
	password = "As123456"

class BlogFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Blog
		sqlalchemy_session = Session   # the SQLAlchemy session object

	title="Test Title"
	content = "Test Content"
	author = factory.SubFactory(UserFactory)	


class CommentTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestingConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()                      
		cls.app_context.push()       
		db.create_all()
		cls.session = Session()
		blog= BlogFactory()
		cls.session.commit()

	@classmethod 	
	def tearDownClass(cls):
		cls.session.rollback()
		Session.remove()
		db.session.remove()
		db.drop_all()

	def test_comment_form_valid(self):
		
		data = {
				"content" : "This is Test comment"
			}
		commentform = CommentForm(data = data)
		self.assertTrue(commentform.validate(),True)

	def test_comment_form_invalid(self):
		commentform = CommentForm(data = dict())
		self.assertFalse(commentform.validate(),False)

	def test_a_comment_view(self):
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		
		user=User.query.filter_by(username="test").first()
	 	blog =Blog.query.filter_by(author=user).first()
		rv = self.app.post(url_for('mod_blog.detail_blog',
									id=int(blog.id)
								),
							data=dict(
								content="This is test comment",
								),
							follow_redirects=True)
		assert "This is test comment" in rv.data


	def test_b_reply_view(self):
		user=User.query.filter_by(username="test").first()
	 	blog =Blog.query.filter_by(author=user).first()
		comment = Comment.query.filter_by(content="This is test comment").first()

		rv = self.app.post(url_for('mod_blog.detail_blog',
									id=int(blog.id)
								),
							data=dict(
								content="This is test comment reply",
								parent_id = comment.id	
								),
							follow_redirects=True)
		assert "This is test comment reply" in rv.data
