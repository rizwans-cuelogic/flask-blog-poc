import unittest
from flask import Flask,url_for,session
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog,Comment
from ..mod_blog.forms import CommentForm

class CommentTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestingConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()                      
		cls.app_context.push()       
		db.create_all()

	@classmethod 	
	def tearDownClass(cls):
		db.session.remove()
		db.drop_all()

	def create_user(self):
		user = User(username="test",email="test@test.com",password="As123456")
		return user

	def get_user(self):
		user = User.query.filter_by(username='test').first()
		return user

	def test_comment_form_valid(self):
		
		data = {
				"content" : "This is Test comment"
			}
		commentform = CommentForm(data = data)
		print commentform.validate()
		print commentform.errors
		self.assertTrue(commentform.validate(),True)

	def test_comment_form_invalid(self):
		commentform = CommentForm(data = dict())
		self.assertFalse(commentform.validate(),False)

	def test_comment_view(self):
		
		user = self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()

		rv = self.app.post(url_for('mod_blog.detail_blog',
									id=int(blog.id)
								),
							data=dict(
								content="This is test comment",
								),
							follow_redirects=True)
		assert "This is test comment" in rv.data


	def test_reply_view(self):
		user = self.get_user()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)

		blog =Blog.query.filter_by(title="this is test").first()
		comment=Comment(content="This is test comment")
		db.session.add(comment)
		db.session.commit()
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
