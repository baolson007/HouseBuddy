from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, FileField, DateField #Y-m-d
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional
from housebuddy.models import User, MaintenanceItem


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

class AddItemForm(FlaskForm):
    name = StringField(label='Maintenance Item Name', validators=[DataRequired()])
    description = StringField(label='Description', validators=[DataRequired()])
    dueDate = DateField(label='Due Date', validators=[Optional()])
    #completionStatus = db.Column(db.Integer(), default=0, unique=False)
    #completionDate = db.Column(db.DateTime, nullable =True, default=datetime.fromisoformat('1900-01-01'))
    #owner = 
    cost = DecimalField(label='Cost', validators=[Optional()])
    submit = SubmitField(label='Add Item')

class EditItemForm(FlaskForm):
	name = StringField(label='Maintenance Item Name')
	description = StringField(label='Description')
	dueDate=DateField(label='Due Date', validators=[Optional()])
	cost = DecimalField(label='Cost', validators=[Optional()])
	submit = SubmitField(label='Submit Updated Item')
	delete = SubmitField(label='Delete Item')


class ItemDetailForm(FlaskForm):
	name = StringField(label='Maintenance Item Name')
	description = StringField(label='Description')
	notes = StringField(label="Notes")
	dueDate=DateField(label='Due Date')
	cost = DecimalField(label='Cost', validators=[Optional()])
	file = FileField()
	submit = SubmitField(label='Submit Updated Item')

#class UploadForm(FlaskForm):
	#filename = FileField()
	#submit = SubmitField(label = "Upload File")
	##delete = SubmitField(label='Delete File')

class ResetPasswordForm(FlaskForm):
	email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
	submit = SubmitField(label='Request Password Reset')

	def validate_email(self, email_to_validate):
		email = User.query.filter_by(email=email_to_validate.data).first()
		if email is None:
			raise ValidationError(f'Error submitting password reset request for \"{email_to_validate.data}\"')

class NewPasswordForm(FlaskForm):
	password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
	password_confirm = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
	submit = SubmitField(label='Reset Password')

class CalendarForm(FlaskForm):
	dueDate = DateField(label='Due Date', format='%Y-%m-%d', validators=[Optional()])
	completionDate = DateField(label='Completion Date', format='%Y-%m-%d', validators=[Optional()])
	submit = SubmitField(label='Submit')

class DatePickerForm(FlaskForm):
	date = DateField(label='date', format='%Y-%m-%d', validators=[DataRequired()])
	submit = SubmitField(label='Submit')

class UserProfileForm(FlaskForm):
	username = StringField(label='Username', validators=[])
	email = StringField(label='Email', validators=[Email()]) 
	first_name = StringField(label='First Name', validators=[Optional()])
	last_name = StringField(label='Last Name', validators=[Optional()])
	submit = SubmitField(label='Submit')