from flask import render_template,request,session,g,redirect,url_for,flash,abort
from flask_login import login_user,logout_user,login_required,current_user
from urllib2 import HTTPError
import json
from . import mod_user
from .forms import RegisterForm,LoginForm,EditForm
from .models import User
from app.main import main
from app import db
from requests_oauthlib import OAuth2Session
from config import Auth

def get_google_auth(state=None, token=None):
	if token:
		return OAuth2Session(Auth.CLIENT_ID, token=token)
	if state:
		return OAuth2Session(
					Auth.CLIENT_ID,
					state=state,
					redirect_uri=Auth.REDIRECT_URI)
	oauth = OAuth2Session(
				Auth.CLIENT_ID,
				redirect_uri=Auth.REDIRECT_URI,
				scope=Auth.SCOPE
			)
	return oauth


@mod_user.route('/register',methods=['GET','POST'])
def register():

	""" view for registering users """
	
	registerform = RegisterForm()
	loginform = LoginForm()	
	if registerform.validate_on_submit():
		user = User(username=registerform.username.data,
					email=registerform.email.data,
					password=registerform.password.data
					)
		db.session.add(user)
		db.session.commit()
		flash("You have been registered successfully")
		return redirect(url_for('.login'))

	return render_template('register.html',form=registerform)

@mod_user.route('/login',methods=['GET','POST'])
def login():
	
	""" view for users login """
	try:

		login_form=LoginForm()

		if current_user.is_authenticated:
			return redirect(url_for('main.index'))

		google = get_google_auth()
		auth_url, state = google.authorization_url(
								Auth.AUTH_URI, access_type='offline')
		session['oauth_state'] = state
		global oauth_state
		oauth_state = state


		if login_form.validate_on_submit():

			user = User.query.filter_by(email=login_form.email.data).first()
			if user is not None and user.verify_password(login_form.password.data):
				session['remember_me']=login_form.remember_me.data
				login_user(user,login_form.remember_me.data)
				return redirect(url_for('main.index'))
			flash("Invalid Username and Password")	
		return render_template('login.html',title='Login',form=login_form,auth_url=auth_url)

	except:
		
		abort(500)

@mod_user.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('main.index'))


@mod_user.route('/profile/<username>',methods=['GET','POST'])
@login_required
def profile(username):
	
	""" view for editing user profile """

	editform = EditForm()

	if editform.validate_on_submit():
		user = User.query.filter_by(email=current_user.email).first()
		user.username=editform.username.data
		user.email = editform.email.data
		user.Address = editform.address.data
		user.Gender = editform.gender.data
		user.contact = editform.contact.data
		db.session.commit()
		flash('User profile update successfully.')
		return redirect(url_for('.profile',username=current_user))

	else:
		editform.username.data=current_user.username
		editform.email.data = current_user.email
		editform.contact.data = current_user.contact
		editform.address.data = current_user.Address
		editform.gender.data = current_user.Gender

	return render_template('edit_user.html',form=editform)


@mod_user.route('/gCallback')
def callback():
	# Redirect user to home page if already logged in.
	if current_user is not None and current_user.is_authenticated:
		return redirect(url_for('main.index'))

	if 'error' in request.args:
		if request.args.get('error') == 'access_denied':
			return 'You denied access.'
		return 'Error encountered.'
	if 'code' not in request.args and 'state' not in request.args:
		return redirect(url_for('.login'))
	else:
		# Execution reaches here when user has
		# successfully authenticated our app.

		global oauth_state

		google = get_google_auth(state=oauth_state)
		try:
			token = google.fetch_token(
				Auth.TOKEN_URI,
				client_secret=Auth.CLIENT_SECRET,
				authorization_response=request.url)
		except HTTPError:
			return 'HTTPError occurred.'
        
		google = get_google_auth(token=token)
		resp = google.get(Auth.USER_INFO)
		if resp.status_code == 200:
			user_data = resp.json()
			email = user_data['email']
			user = User.query.filter_by(email=email).first()
			if user is None:
				user = User()
				user.email = email
            
			user.username = user_data['name']
			print(token)
			user.tokens = json.dumps(token)
			user.avatar = user_data['picture']
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('main.index'))
		return 'Could not fetch your information.'
