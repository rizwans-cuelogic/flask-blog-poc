import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

	SECRET_KEY = "you-will-never-guess"



class DevelopmentConfig(Config):
	
	DEBUG = True
	WTF_CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/blog"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):

	DEBUG = True

class TestingConfig(Config):

	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/blog_test"
	SQLALCHEMY_TRACK_MODIFICATIONS = False