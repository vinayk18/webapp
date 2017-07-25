from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,DateField,IntegerField
from wtforms.validators import Required, Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from  ..models import Branch,Election

BRANCH_CHOICES =[('CSE','COMPUTER SCIENCE AND ENGINEERING'),('MECH','MECHANICAL ENGINEERING'),('ECE','ELECTRONIC AND COMMUNICATION ENGINEERING'),('EEE','ELECTRICAL ENGINEERING'),('CIV','CIVIL ENGINEERING'),('CHEM','CHEMICAL ENGINEERING'),('MSME','MATERIAL SCIENCE AND METTALURGICAL ENGINEERING'),('ARCH','ARCHITECTURE'),('PLAN','PLANNING')]

SEM_CHOICES = [('ONE',1),('TWO',2),('THREE',3),('FOUR',4),('FIVE',5),('SIX',6),('SEVEN',7),('EIGHT',8)]

class CandidateForm(FlaskForm):
	name = StringField('name',validators = [Required()])
	branch = SelectField('branch',validators = [Required()], choices = BRANCH_CHOICES)
	semester = IntegerField('Semester', validators =[Required()])
	scholarNo = StringField('Scholar ID', validators = [Required(), Length(9,9)])
	submit = SubmitField('submit')
	
	def validate_branch(self,field):
		if not Branch.query.filter_by(name = self.branch.data).filter_by(semester = self.semester.data).first():
			raise ValidationError('It seems like there is no election for this branch and semester yet.Make sure the election is being held on.')
	
	def validate_scholarNo(self,field):
		if Election.query.filter_by(sid = self.scholarNo.data).first():
			raise ValidationError('scholar id already present')

class NewElecForm(FlaskForm):
	branch = SelectField('branch',validators = [Required()], choices = BRANCH_CHOICES)
	sem = IntegerField('Semester',validators=[Required()])
	date = DateField('Date of election', format='%m/%d/%Y')
	submit = SubmitField('submit')

class ChangePasswordForm(FlaskForm):
	old_password =	PasswordField(' Old Password', validators=[Required()])
	password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm New Password', validators=[Required()])
	submit = SubmitField('Submit')	

class ChangeEmailForm(FlaskForm):
	email = StringField('Email',validators = [Required(),Length(1,64),Email(),EqualTo('email2', message='Email IDs must match.')])
	email2 = StringField('Confirm Email',validators = [Required(),Length(1,64),Email()])
	submit = SubmitField('Submit')