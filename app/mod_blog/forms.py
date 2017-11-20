import datetime

from flask_wtf import Form
from wtforms_components import DateRange
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo,optional
from app.mod_user.models import User,Blog


class BlogForm(Form):

	title = StringField('Title',validators=[DataRequired(),Length(1,128)])
	content =TextAreaField('Content',validators=[DataRequired()])
	publication_date = DateField('publicaion_date',format='%Y/%m/%d',
								validators=[optional(),DateRange(
																min = datetime.date.today()
																)])
	submit = SubmitField('Post')