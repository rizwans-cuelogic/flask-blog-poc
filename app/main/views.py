from flask import request,render_template,session,g,abort,redirect
from flask_login import current_user
from app.mod_user.models import Blog,User
from . import main

@main.route('/')
def index():
	"""  index page """	
	blogs=[]
	if current_user.is_authenticated:
		blogs = current_user.blogs.all()

	return render_template('index.html',blogs=blogs)