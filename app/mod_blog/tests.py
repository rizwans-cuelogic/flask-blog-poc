import unittest
from flask import Flask,url_for
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog
from ..mod_blog.forms import BlogForm


class BlogTestCase(unittest.TestCase):
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
		user =  User(username="test",email="test@test.com",password="As123456")
		return user

	def get_user(self):
		user = User.query.filter_by(username='test').first()
		return user	

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


	def test_add_blog(self):
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
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

	def test_list_blog(self):
		user= self.get_user()
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()			
		rv = self.app.get('/listblog',follow_redirects=True)
		assert "this is test" in rv.data


	def test_edit_blog(self):
		user= self.get_user()
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()
		rv = self.app.post(url_for('mod_blog.edit_blog',
									id=int(blog.id)),
							data=dict(
								title="editing blog",
								content="thid edited content"
								),
							follow_redirects=True)
		assert "Blog Updated Successfully" in rv.data

	def test_blog_detail(self):
		user= self.get_user()
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()
		rv = self.app.get(url_for('mod_blog.detail_blog',
									id=int(blog.id)),
									follow_redirects=True
							)	
 		assert "this test content" in rv.data

 	def test_all_blog(self):
 	 	user= self.get_user()
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()
		rv = self.app.get('/allblog',follow_redirects=True)
		assert "this is test" in rv.data


	def test_delete_blog(self):
		user= self.get_user()
		blogs = Blog.query.delete()
		blog =Blog(title="this is test",content="this test content",author=user)
		db.session.add(blog)
		db.session.commit()
		rv =self.app.get(url_for('mod_blog.delete_blog',id=blog.id),follow_redirects=True)

		assert "you dont have any blog" in rv.data	

	def test_list_blog_empty(self):
		user= self.get_user()
		blogs = Blog.query.delete()
		rv = self.app.get('/listblog',follow_redirects=True)
		assert "you dont have any blog" in rv.data

