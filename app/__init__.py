from flask import Flask
from flask_admin import Admin 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection ='Strong'

admin = Admin(app, name='blogger', template_mode='bootstrap3')

from . import urls

from app.mod_user import views,models
from app.main import views 
from app.mod_blog import views

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Blog, db.session))