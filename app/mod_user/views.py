from flask import render_template,request,session,g,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user

from . import mod_user
from .forms import RegisterForm,LoginForm,EditForm
from .models import User
from app.main import main
from app import db

@mod_user.route('/register',methods=['GET','POST'])
def register():
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
	login_form=LoginForm()

	if login_form.validate_on_submit():

		user = User.query.filter_by(email=login_form.email.data).first()
		if user is not None and user.verify_password(login_form.password.data):
			session['remember_me']=login_form.remember_me.data
			login_user(user,login_form.remember_me.data)
			return redirect(url_for('main.index'))
		flash("Invalid Username and Password")	
	return render_template('login.html',title='Login',form=login_form)

@mod_user.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('main.index'))


@mod_user.route('/profile/<username>',methods=['GET','POST'])
@login_required
def profile(username):
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