from flask import Flask,redirect,url_for,flash
from flask_admin import Admin,AdminIndexView,expose 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user,login_user,logout_user
from flask_admin.contrib.sqla import ModelView
from .momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.jinja_env.globals['momentjs'] = momentjs


db = SQLAlchemy(app)
lm = LoginManager(app)
lm.session_protection ='Strong'


from . import urls

from app.mod_user import views,models,forms
from app.main import views 
from app.mod_blog import views

class MyModelView(ModelView):

	def is_accessible(self):
		return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):

	@expose('/')
	def index(self):
		user = models.User.query.filter_by(email="Admin@example.com").first()
		if user is None:
			user = models.User(username="Admin",email="Admin@example.com",password="Admin123")
			db.session.add(user)
			db.session.commit()

		if not current_user.is_authenticated or not current_user.email=='Admin@example.com':
			return redirect(url_for('.login_view'))
		return super(MyAdminIndexView, self).index()

	@expose('/login/', methods=('GET', 'POST'))
	def login_view(self):
		# handle user login
		form = forms.LoginForm()
		if form.validate_on_submit():
			user = models.User.query.filter_by(email="Admin@example.com").first()
			if form.email.data =="Admin@example.com" and form.password.data=="Admin123":
				login_user(user)
				return redirect(url_for('.index'))
			flash("Invalid Username and Password")	
		
		self._template_args['form'] = form
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		logout_user()
		return redirect(url_for('.index'))	

admin = Admin(app, name='blogger', index_view=MyAdminIndexView(),base_template="my_master.html",template_mode='bootstrap3')

admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Blog, db.session))
