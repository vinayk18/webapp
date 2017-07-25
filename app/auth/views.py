from flask import render_template, redirect, request, url_for, flash ,abort
from flask_login import login_user,logout_user, login_required,current_user
from . import auth
from .. import db
from ..models import User , Branch,Election
from ..email import send_email
from .forms import LoginForm ,RegistrationForm,EditProfileForm,ChangePasswordForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(s_no=form.scholarNo.data).first()
		if user is not None and user.is_admin == True and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(url_for('admin.index'))
		if user is not None and user.is_admin == False and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid user ID or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))	

@auth.route('/profile/<scholarNo>')
@login_required
def profile(scholarNo):
	user = User.query.filter_by(s_no = scholarNo).first()
	if user is None:
		abort(404)
	return render_template('auth/profile.html',user = user)

@auth.route('/elections/<branch>/<semester>',methods = ['GET','POST'])
@login_required
def elections(branch,semester):
	cand = Branch.query.filter_by(name = branch).filter_by(semester = semester).first()
	if cand is None:
		abort(404)
	list = Election.query.filter_by(branch = branch).filter_by(sem = semester).all()	
	return render_template('auth/elections.html',list = list)	

@auth.route('/register',methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,username=form.username.data,branch =form.branch.data,semester = form.semester.data,s_no = form.scholarNo.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form = form)
	
@auth.route('/vote/<voter>/<candidate>',methods = ['GET','POST'])
@login_required
def vote(voter,candidate):
	user  = User.query.filter_by(s_no = voter).first()
	if user.has_voted == True:
		flash('You cannot vote more than once')
		return redirect(url_for('auth.elections',branch = user.branch,semester = user.semester))
	user.has_voted = True
	candi = Election.query.filter_by(sid = candidate).first()
	candi.votes = candi.votes + 1
	db.session.commit()
	return 'Thank you '

@auth.route('/edit-profile/',methods = ['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your profile has been updated.')
		return redirect(url_for('auth.profile', scholarNo = current_user.s_no))
	form.username.data = current_user.username
	form.email.data = current_user.email
	return render_template('auth/edit_profile.html', form=form)

@auth.route('/change-password/<scholarNo>/',methods = ['GET','POST'])	
@login_required
def change_password(scholarNo):
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(s_no = scholarNo).first()
		if user is not None and user.verify_password(form.old_password.data):
			user.password = form.password.data
			db.session.add(user)
			db.session.commit()
			flash('Your Password has been updated')
		return redirect(url_for('auth.profile',scholarNo = scholarNo))
		flash('Invalid Old Password')
	return render_template('auth/change_password.html',form = form)	
	
@auth.route('/view-results/<branch>/<semester>/',methods = ['GET','POST'])
@login_required
def view_results(branch,semester):
	cand = Election.query.filter_by(branch = branch).filter_by(sem=semester).all()
	list = [iter.votes for iter in cand]
	max_vote = max(list)
	cand = Election.query.filter_by(branch = branch).filter_by(sem = semester).filter_by(votes = max_vote).first()
	return render_template('auth/view_results.html',CR = cand)