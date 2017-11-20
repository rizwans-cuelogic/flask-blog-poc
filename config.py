import os

base_dir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"

SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False