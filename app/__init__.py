from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection ='Strong'

from . import urls

from app.mod_user import views,models
from app.main import views 
from app.mod_blog import views
