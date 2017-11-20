from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,Length,EqualTo
from .models import User,Blog

GENDER =[('Male','M'),('Female','F')]

class RegisterForm(Form):
	
	""" Registerform for registering users """

	username = StringField('Username',validators=[DataRequired()]) 
	email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(1,64),EqualTo('confirm_password',message="Password must match.")])
	confirm_password =PasswordField('confirm_password',validators=[DataRequired()])
	submit = SubmitField("Register")


class LoginForm(Form):
	
	""" Loginform for users login """

	email = StringField('Email',validators=[ DataRequired(),Length(1,64),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me',default=False)
	submit= SubmitField("Log In")


class EditForm(Form):
	
	""" Editform for editing users profile """

	username = StringField("username",validators=[DataRequired()])
	email = StringField("email",validators=[DataRequired(),Length(1,64),Email()])
	contact = StringField("contact",validators=[Length(0,12)])
	address = TextAreaField("address")
	gender = SelectField("Gender",choices=GENDER)
	submit= SubmitField("Save Profile")	