from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import Required, Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from  ..models import User

BRANCH_CHOICES =[('CSE','COMPUTER SCIENCE AND ENGINEERING'),('MECH','MECHANICAL ENGINEERING'),('ECE','ELECTRONIC AND COMMUNICATION ENGINEERING'),('EEE','ELECTRICAL ENGINEERING'),('CIV','CIVIL ENGINEERING'),('CHEM','CHEMICAL ENGINEERING'),('MSME','MATERIAL SCIENCE AND METTALURGICAL ENGINEERING'),('ARCH','ARCHITECTURE'),('PLAN','PLANNING')]

SEM_CHOICES = [('1','ONE'),('2','TWO'),('3','THREE'),('4','FOUR'),('5','FIVE'),('6','SIX'),('7','SEVEN'),('8','EIGHT')]

class LoginForm(FlaskForm):
	scholarNo = StringField('Scholar Id', validators =[Required(),Length(min=9,max=9)])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email',validators = [Required(),Length(1,64),Email()])
	username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters,''numbers, dots or underscores')]) 
	scholarNo = StringField('Scholar Id', validators =[Required(),Length(9,9)])
	branch = SelectField('Branch',choices =BRANCH_CHOICES,validators =[Required()])
	semester = SelectField('Semester',choices = SEM_CHOICES,validators =[Required()])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')
 
	def validate_email(self, field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email already registered.')
	
	def validate_scholarNo(self,field):
		if User.query.filter_by(s_no = field.data).first():
			raise ValidationError('Scholar ID already registered.') 	
		
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')		

class EditProfileForm(FlaskForm):
	username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters,''numbers, dots or underscores')]) 
	email = StringField('Email',validators = [Required(),Length(1,64),Email()])
	submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
	old_password =	PasswordField(' Old Password', validators=[Required()])
	password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm New Password', validators=[Required()])
	submit = SubmitField('Submit')