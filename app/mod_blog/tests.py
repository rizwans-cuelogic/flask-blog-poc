import unittest
import factory
import config
from flask import Flask,url_for
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog
from ..mod_blog.forms import BlogForm
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

class BlogTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestingConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()                      
		cls.app_context.push()       
		db.create_all()
		cls.session = Session()
		user= UserFactory()
		cls.session.commit()

	@classmethod 	
	def tearDownClass(cls):
		cls.session.rollback()
		Session.remove()
		db.session.remove()
		db.drop_all()

	def test_addblog_url(self):
		rv = self.app.get('/addblog')
		self.assertTrue(rv.status_code,401)

	def test_editblog_url(self):
		rv = self.app.get('/editblog')
		self.assertTrue(rv.status_code,401)

	def test_deleteblog_url(self):
		rv = self.app.get('/deleteblog')
		self.assertTrue(rv.status_code,401)

	def test_listblog_url(self):
		rv = self.app.get('/listblog')
		self.assertTrue(rv.status_code,401)

	def test_blogform_valid(self):
		data = {
				"title":"This is Test blog.",
				"content" : "This is Test content"
				}
		blogform = BlogForm(data = data)
		self.assertTrue(blogform.validate(),True)

	def test_blogform_invalid(self):
		data = {
				"content" : "This is Test content"
				}
		blogform = BlogForm(data = data)
		self.assertFalse(blogform.validate(),False)


	def test_a_add_blog(self):
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		rv = self.app.post('/addblog',
							data=dict(
								title="this is test blog",
								content="this is test content"	
								),follow_redirects=True)
		assert "Added blog successfully" in rv.data

	def test_b_list_blog(self):
		
		user=User.query.filter_by(username="test").first()			
		rv = self.app.get('/listblog',follow_redirects=True)
		assert "this is test" in rv.data
		

	def test_c_edit_blog(self):
		user=User.query.filter_by(username="test").first()
	 	blog =Blog.query.filter_by(author=user).first()
		rv = self.app.post(url_for('mod_blog.edit_blog',
									id=int(blog.id)),
							data=dict(
								title="editing blog",
								content="thid edited content"
								),
							follow_redirects=True)
		assert "Blog Updated Successfully" in rv.data

	def test_c_blog_detail(self):
		user=User.query.filter_by(username="test").first()
	 	blog =Blog.query.filter_by(author=user).first()
		rv = self.app.get(url_for('mod_blog.detail_blog',
									id=int(blog.id)),
									follow_redirects=True
							)	
 		assert "this is test content" in rv.data
 		
 	def test_d_all_blog(self):
		rv = self.app.get('/allblog',follow_redirects=True)
		assert "editing blog" in rv.data

	def test_e_delete_blog(self):
		user=User.query.filter_by(username="test").first()
	 	blog =Blog.query.filter_by(author=user).first()
		rv =self.app.get(url_for('mod_blog.delete_blog',id=int(blog.id)),follow_redirects=True)

		assert "you dont have any blog" in rv.data	

	def test_list_blog_empty(self):
		rv = self.app.get('/listblog',follow_redirects=True)
		assert "you dont have any blog" in rv.data

