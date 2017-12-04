import unittest
import factory
import config
from flask import Flask,url_for
from .. import app,db,mod_user
from ..mod_user.models import User
from .forms import RegisterForm,LoginForm,EditForm
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



class UserTestCase(unittest.TestCase):
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
		user= self.session.query(User).filter_by(username="test").first()
		assert user in self.session

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
		user= self.session.query(User).filter_by(username="test").first()
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
