from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection ='Strong'

from app.mod_user import mod_user as user_blueprint
from app.main import main as main_blueprint
from app.mod_blog import mod_blog as blog_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(blog_blueprint)

from app.mod_user import views,models
from app.main import views 
from app.mod_blog import views
