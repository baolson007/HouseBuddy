from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from housebuddy.models import User


class RegisterForm(FlaskForm):

	def validate_username(self, username_to_validate):
		user = User.query.filter_by(username=username_to_validate.data).first()
		if user:
			raise ValidationError(f'Username \"{username_to_validate.data}\" already exists, please a different username')

	def validate_email(self, email_to_validate):
		email = User.query.filter_by(email=email_to_validate.data).first()
		if email:
			raise ValidationError(f'Email address \"{email_to_validate.data}\" already exists, please try different email address')

	username = StringField(label='User Name:', validators=[Length(min=2, max=40), DataRequired()])
	email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
	password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
	password_confirm = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
	submit = SubmitField(label='Register Account')

class LoginForm(FlaskForm):
	username = StringField(label='User Name:', validators=[DataRequired()])
	password = PasswordField(label='Password:', validators=[DataRequired()])
	submit = SubmitField(label='Sign in to HouseBuddy!')