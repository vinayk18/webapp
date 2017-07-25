from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField , PasswordField , SelectField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
	