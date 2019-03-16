import os
import csv
import secrets
import pandas as pd
# import numpy as np
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_file, jsonify
from scoreapp import app, db, bcrypt
from scoreapp.forms import LoginForm
from scoreapp.models import order, shippingData, registrationData, marketing, jobs, teamUser, masterData
from flask_login import login_user, current_user, logout_user, login_required
from scoreapp.job_helper import *
from sqlalchemy import desc

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	image_file = url_for('static', filename='img/paytm_logo.png')
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = teamUser.query.filter_by(username=form.username.data).first()
		print(user)
		if user and user.password == form.password.data:
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form, logo = image_file)


@app.route("/home")
@login_required
def home():
	print("home called")
	jobq = jobs.query.filter_by(job_status='active')
	return render_template('home.html', title='Index', jobs=jobq)

# @app.route("/run/<string:category>")
# def run(category=None):
# 	if category is None:
# 		self.Error(400)
# 	try:
# 		jobq = jobs.query.filter_by(job_status='active')
# 		return render_template('home.html', title='Index', jobs=jobq)
# 	except Exception as e:
# 		self.log.exception(e)
# 		self.Error(400)


@app.route("/run/<string:category>")
def run(category=None):
	if category is None:
		self.Error(400)
	try:
		# run and save job
		job_data = detect_active_job(category)
		if(len(job_data)>0):
			flash("Already Added")
		else:
			job_data = jobs.query.filter_by(job_name=category).order_by(desc(jobs.start_time)).first()
			job_start_time = job_data.start_time
			job_status= job_data.job_status
			job_id= job_data.job_id
			job_finish_time = job_data.finish_time
			job_total_records = job_data.total_records
			job_currently_processed_record = job_data.currently_processed_records
			print(job_id)
			print(job_status)


		# # refresh page
		#jobq = jobs.query.filter_by(job_status='active')
		return redirect(url_for('home'))
	except Exception as e:
		self.log.exception(e)
		self.Error(400)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route("/dataloader")
def load_data():
	#file = pd.read_csv('scoreapp/data.csv')
	#print(file.head())
	file_name = 'scoreapp/data.csv'
	with open(file_name) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag = 0
		cnt = 0
		for row in csv_reader:
			cntt = 0
			if flag:
				md = masterData(id=row[1], age=int(row[0]), is_auto_billing=int(row[2]), is_paytm_first=int(row[3]),
								is_postpaid=int(row[4]), postpaid_outstanding=int(row[5]),
								orders_placed_in_6months=int(row[6]),
								orders_placed_in_6months_via_epay=int(row[7]),
								orders_placed_in_6months_via_cod=int(row[8]),
								orders_placed_in_6months_via_emi=int(row[9]), orders_delivered_in_6months=int(row[10]),
								total_money_on_order_from_mall_6months=int(row[11]),
								total_money_on_order_on_travel_6months=int(row[12]),
								total_money_on_order_on_movie_6months=int(row[13]), total_money_spent=int(row[14]),
								total_money_added_on_wallet=int(row[15]), CODorNot=int(row[16]), EMIorNot=int(row[17]),
								RatioDvP=float(row[18]))
				db.session.add(md)
				db.session.commit()
				cnt += 1
				print(cnt)				
			flag = 1