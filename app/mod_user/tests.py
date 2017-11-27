import unittest
from flask import Flask,url_for
from .. import app,db,mod_user
from ..mod_user.models import User
from .forms import RegisterForm,LoginForm,EditForm

class UserTestCase(unittest.TestCase):
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

	def test_adduser(self):
		user= self.create_user()
		db.session.add(user)
		db.session.commit()
		assert user in db.session

	def test_register_valid(self):
		rv = self.app.post('/register', data=dict(
				email="test1@test.com",
				username="test1",
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
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Hi,test" in rv.data

	def test_logout(self):
		email="test@test.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		rv = self.app.get('/logout', 
						follow_redirects=True)
		assert "You have been logged out" in rv.data


	def test_login_invalid(self):
		email="test@t.com"
		password="As123456"
		rv = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Invalid Username and Password" in rv.data


	def test_profile(self):
		user= self.get_user()
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
