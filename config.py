import os

base_dir = os.path.abspath(os.path.dirname(__file__))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Auth:
	CLIENT_ID = ('607173259185-r9gju8166ccn74s76lq3b930mbvdrkif'
					'.apps.googleusercontent.com')
	CLIENT_SECRET = 'n1j_EAYN5e5x-B5BsPEWvTqC'
	REDIRECT_URI = 'http://localhost:8085/gCallback'
	AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
	TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
	USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
	SCOPE = [
		'https://www.googleapis.com/auth/userinfo.email',	
		'https://mail.google.com/',
		'https://www.googleapis.com/auth/gmail.compose',
		'https://www.googleapis.com/auth/gmail.send',
		'https://www.googleapis.com/auth/gmail.insert',
		'https://www.googleapis.com/auth/gmail.labels',
		'https://www.googleapis.com/auth/gmail.modify',
		'https://www.googleapis.com/auth/plus.login',
		'https://www.googleapis.com/auth/gmail.modify',
		'https://www.googleapis.com/auth/gmail.settings.sharing',
		'https://www.googleapis.com/auth/gmail.settings.basic'
	]



class Config(object):

	SECRET_KEY = "you-will-never-guess"



class DevelopmentConfig(Config):
	
	DEBUG = True
	WTF_CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/blog"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'prompt': 'select_account'}
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class ProductionConfig(Config):

	DEBUG = True

class TestingConfig(Config):

	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/blog_test"
	SQLALCHEMY_TRACK_MODIFICATIONS = False