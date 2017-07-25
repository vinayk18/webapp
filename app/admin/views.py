from flask import render_template, redirect, request, url_for, flash 
from flask_login import login_user,logout_user, login_required,current_user
from .forms import CandidateForm,NewElecForm,ChangePasswordForm,ChangeEmailForm
from .. import db
from ..models import Election,Branch,User
from . import admin

@admin.route('/home')
def index():
	return render_template('admin/admin.html',)

@admin.route('/elections')
@login_required
def elections():
	bran = Branch.query.all()
	return render_template('admin/elections.html',branches = bran)		
	
@admin.route('/',methods = ['GET','POST'])
@login_required
def new_election():
	form = NewElecForm()
	if form.validate_on_submit():
		bran = Branch(name = form.branch.data,semester=form.sem.data,Date=form.date.data)
		db.session.add(bran)
		db.session.commit()
		return '<h1>Done!</h1>'
	return render_template('admin/new_election.html',form = form)
	
@admin.route('/view-election/<branch>/<semester>/',methods = ['GET','POST'])	
@login_required
def view_election(branch,semester):
	cand = Branch.query.filter_by(name = branch).filter_by(semester = semester).first()
	if cand is None:
		abort(404)
	list = Election.query.filter_by(branch = branch).filter_by(sem = semester).all()	
	return render_template('admin/view_election.html',list = list)	
		

@admin.route('/add-candi/',methods= ['GET','POST'])
@login_required
def add_candidate():
	form = CandidateForm()
	if form.validate_on_submit():
		candi = Election(name = form.name.data,branch = form.branch.data,sid = form.scholarNo.data,sem=form.semester.data)
		db.session.add(candi)
		db.session.commit()
		flash('Candidate has been added.')
		return redirect(url_for('admin.elections'))
	return render_template('admin/add_candidate.html',form=form) 
	
@admin.route('/delete-candidate/<scholarNo>/',methods =['GET','POST'])
@login_required
def delete_candidate(scholarNo):
	one = Election.query.filter_by(sid = scholarNo).first()
	db.session.delete(one)
	db.session.commit()
	flash('Candidate has been deleted.')
	return redirect(url_for('admin.elections'))
	
@admin.route('/change-password/<scholarNo>/',methods = ['GET','POST'])	
@login_required
def change_password(scholarNo):
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(s_no = scholarNo).first()
		if user is not None and user.verify_password(form.old_password.data):
			user.password = form.password.data
			db.session.add(user)
			db.session.commit()
			flash('Your password has been updated')
			return render_template('admin/admin.html')
		flash('Invalid Old Password')	
	return render_template('admin/change_password.html',form = form)	

@admin.route('/change-email')
@login_required
def change_email():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		current_user.email = form.password.data
		db.session.commit()
		flash('Your password has been updated')
		return redirect(url_for('admin.index'))
	return render_template('admin/change_email.html',form = form) 

	
