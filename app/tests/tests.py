import os
import unittest
from flask import Flask,url_for
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog
from flask_testing import TestCase
from ..mod_user.forms import LoginForm,RegisterForm,EditForm
from ..mod_blog.forms import BlogForm


class TestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
		self.app = app.test_client()
		self.app_context = app.test_request_context()                      
		self.app_context.push()       
		db.create_all()
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	
	def create_user(self):
		user = User(username="test",email="test@test.com",password="As123456")
		return user

	""" url testing """

	def test_index_url(self):
		rv = self.app.get('/')
		self.assertTrue(rv.status_code,200)

	def test_register_url(self):
		rv = self.app.get('/register')
		self.assertTrue(rv.status_code,200)

	def test_login_url(self):
		rv = self.app.get('/login')
		self.assertTrue(rv.status_code,200)

	def test_logout_url(self):
		rv = self.app.get('/logout')
		self.assertTrue(rv.status_code,401)	
		
	def test_user_profile_url(self):
		rv = self.app.get(url_for('mod_user.profile',username='test'))
		self.assertTrue(rv.status_code,401)

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

	""" form testing """	

	def test_loginform_valid(self):
		data = {'email':"test@test.com",
				'password':"As123456"}
		loginform = LoginForm(data=data)
		self.assertTrue(loginform.validate(),True)		

	def test_loginform_invalid(self):
		data={'password':"As123456"}
		loginform = LoginForm(data=data)
		self.assertFalse(loginform.validate(),False)

	def test_registerform_valid(self):
		data = {'username':"test",
				'email':'test@test.com',
				'password':'test123',
				'confirm_password':'test123'
				}
		registerform = RegisterForm(data=data)
		self.assertTrue(registerform.validate(),True)

	def test_registerform_invalid(self):
		data = {'email':'test@test.com',
				'password':'test123',
				'confirm_password':'test123'
				}
		registerform = RegisterForm(data=data)
		self.assertFalse(registerform.validate(),False)

	def test_editform_valid(self):
		data =  {'username':"test",
				'email':'test@test.com',
				'address':'123,abc street',
				'contact':'123456789011',
				'gender':'Male',
				}
		editform = EditForm(data=data)
		self.assertTrue(editform.validate(),True)

	def test_editform_invalid(self):
		data =  {
				'email':'test@test.com',
				'address':'123,abc street',
				'contact':'123456789011',
				'gender':'Male',
				}
		editform = EditForm(data=data)
		self.assertFalse(editform.validate(),False)

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

	
	""" views testing """

	def test_adduser(self):
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		assert user in db.session

	def test_register_valid(self):
		rv = self.app.post('/register', data=dict(
				email="test@test.com",
				username="test",
				password="test123456",
				confirm_password="test123456"
			), follow_redirects=True)
		assert "You have been registered successfully" in rv.data

	def test_register_invalid(self):
		rv = self.app.post('/register', data=dict(
				username="test",
				password="test123456",
				confirm_password="test123456"
			), follow_redirects=True)
		assert "This field is required." in rv.data	

	def test_login_valid(self):
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Hi,test" in rv.data

	def test_login_invalid(self):
		
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@t.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Invalid Username and Password" in rv.data

	def test_logout(self):

		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		rv = self.app.get('/logout', 
						follow_redirects=True)
		assert "You have been logged out" in rv.data

	def test_profile(self):
		
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)

		rv = self.app.post(url_for('mod_user.profile',
							username=user.username),
							data=dict( username=user.username,
										email=user.email,
										address="abcstreet123",
										gender="Male"),
							follow_redirects=True)
		assert "User profile update successfully." in rv.data

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
					
		rv = self.app.get('/listblog',follow_redirects=True)

		assert "this is test blog" in rv.data

	def test_list_blog_empty(self):
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
					
		rv = self.app.get('/listblog',follow_redirects=True)

		assert "you dont have any blog" in rv.data

	def test_delete_blog(self):
		user= self.create_user()
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
		rv =self.app.get(url_for('mod_blog.delete_blog',id=blog.id),follow_redirects=True)

		assert "you dont have any blog" in rv.data

	def test_edit_blog(self):
		user= self.create_user()
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
		rv = self.app.post(url_for('mod_blog.edit_blog',
									id=int(blog.id)),
							data=dict(
								title="editing blog",
								content="thid edited content"
								),
							follow_redirects=True)
		assert "Blog Updated Successfully" in rv.data

	def test_blog_detail(self):
		user= self.create_user()
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
		rv = self.app.get(url_for('mod_blog.detail_blog',
									id=int(blog.id)),
									follow_redirects=True
							)	
 		assert "this test content" in rv.data

 	def test_all_blog(self):
 		user= self.create_user()
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
		rv = self.app.get('/allblog',follow_redirects=True)
		assert "this is test" in rv.data




if __name__ == '__main__':
	unittest.main()