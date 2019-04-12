from flask import Flask, request, render_template, flash, redirect, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form, FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextField, SelectField, DateField
from wtforms.validators import InputRequired, Optional, Email, Length

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, DateTime, desc
from flaskext.mysql import MySQL

from flask_bootstrap import Bootstrap
from flask_caching import Cache

import datetime

app = Flask(__name__)
app.secret_key = '\xa3;\xf1G\xf8\x1a\xd1\x81d\x99JW\x16\x98\x7f'
app.config['DEBUG'] = True

mysql = MySQL()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:user@localhost:3306/database'
mysql.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class LoginForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class Orders(db.Model):
	__tablename__ = "Orders"
	id = db.Column('id', db.Integer, primary_key=True)
	current_stage = db.Column('current_stage', db.Integer)
	status = db.Column('status', db.Integer)
	cust_name = db.Column('cust_name', db.Text())
	site_name = db.Column('site_name', db.Text())
	site_num = db.Column('site_num', db.Text())

	def __repr__(self):
		return '<Order %r>' % self.id

class Substages(db.Model):
	__tablename__ = "Substages"
	id = db.Column('id', db.Integer, primary_key=True)
	stage = db.Column('stage', db.Integer)
	substage = db.Column('substage', db.Text())

	def __repr__(self):
		return '<SubStage %r>' % self.id

class Order_Substages(db.Model):
	__tablename__ = "Order_Substages"
	id = db.Column('id', db.Integer, primary_key=True)
	order_id = db.Column('order_id', db.Integer)
	substage_id = db.Column('substage_id', db.Integer)
	stage = db.Column('stage', db.Integer)
	data = db.Column('data', db.Text())

class Enquiries(db.Model):
	__tablename__ = "Enquiries"
	id = db.Column('id', db.Integer, primary_key=True)
	customer = db.Column('customer', db.Text())
	contact_name = db.Column('contact_name', db.Text())
	contact_number = db.Column('contact_number', db.Text())
	contact_email = db.Column('contact_email', db.Text())
	site = db.Column('site', db.Text())
	site_number = db.Column('site_number', db.Text())
	follow_up_date = db.Column('follow_up_date', db.Text())
	priority = db.Column('priority', db.Integer())
	notes = db.Column('notes', db.Text())
	logged_by = db.Column('logged_by', db.Text())
	entered_date = db.Column('entered_date', db.DateTime())

	def __repr__(self):
		return '<Enquiry %r>' % self.id

class Notifications(db.Model):
	__tablename__ = "Notifications"
	id = db.Column('id', db.Integer, primary_key=True)
	datetime = db.Column('datetime', db.DateTime())
	logged_by = db.Column('logged_by', db.Text())
	priority = db.Column('priority', db.Integer())

	def __repr__(self):
		return '<Notifications %r>' % self.id

class newEnquiryForm(Form):
	customer = TextField('Customer:', validators=[InputRequired()])
	contact_name = TextField('Contact Name:', validators=[InputRequired()])
	contact_number = TextField('Contact Number:', validators=[Optional()])
	contact_email = TextField('Contact Email:', validators=[Optional()])
	site = TextField('Site:', validators=[Optional()])
	site_number = TextField('Site Number:', validators=[Optional()])
	follow_up_date = TextField('Follow Up Date', validators=[Optional()])
	priority = SelectField(
		'Priority',
		choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low')], 
		default=2, validators=[Optional()])
	notes = TextField('Notes:', validators=[Optional()])
	logged_by = TextField('Logged By:', validators=[Optional()])

ncounter = 0
@app.context_processor
@cache.cached(timeout=1)
def count():
	global ncounter
	return dict(ncounter=ncounter)

counter = 0
@app.route('/check_for_notifications', methods= ['GET'])
def check_for_notifications():
	global counter

	# check if an enquiry has been logged in the last 5 seconds
	newest_enquiry=db.session.query(Enquiries).order_by('entered_date desc').first()
	if newest_enquiry.entered_date > datetime.datetime.now() - datetime.timedelta(seconds=6):
		print 'yep'
		notification=dict(counter=counter+1, notification='New enquiry logged by '+newest_enquiry.logged_by)
		return render_template('bootstrap-notify.html', notification=notification)
	else:
		notification=dict(counter=counter, notification='')
		return render_template('bootstrap-notify.html', notification=notification)

################################################

@app.route('/')
@login_required
def index():
	# user = User.query.filter_by(username='GAry').first()
	# login_user(user)
	print 'logged in'
	# 20 estimates with nearest follow-up date, sorted by foolow up date then priority
	enquiries = Enquiries.query.order_by(Enquiries.follow_up_date.asc(), Enquiries.priority.asc()).limit(20)

	return render_template('dashboard.html', enquiries=enquiries)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect('/')

		return '<h1>Invalid email or password</h1>'
		#return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		try:
			hashed_password = generate_password_hash(form.password.data, method='sha256')
			new_user = Users(email=form.email.data, password=hashed_password)
			db.session.add(new_user)
			db.session.commit()
			flash('New user created for '+form.email.data)
			return redirect('/')
		except:
			return 'Account already exists for user ' + form.email.data
		#return '<h1>' + form.username.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'

	return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

# enquiries
@app.route('/enquiries')
@login_required
def enquiries():
	# select all enquiries
	data = Enquiries.query.all()

	return render_template('enquiries.html', data=data)

# estimates
@app.route('/estimates')
@login_required
def estimates():
	# select all enquiries
	# data = Estimates.query.all()

	return render_template('estimates.html')#, data=data)

# new enquiry
@app.route("/new", methods=['GET', 'POST'])
@login_required
def newEnquiry():
	global ncounter
	form = newEnquiryForm()
 
	if request.method == 'POST':
		entered_date=datetime.datetime.now()
		customer=request.form['customer']
		contact_name=request.form['contact_name']
		contact_number=request.form['contact_number']
		contact_email=request.form['contact_email']
		site=request.form['site']
		site_number=request.form['site_number']
		follow_up_date=request.form['follow_up_date']
		priority=request.form['priority']
		notes=request.form['notes']
		logged_by=request.form['logged_by']
		
		if form.validate():
			if not follow_up_date:
				follow_up_date = None
			else:
				follow_up_date = datetime.datetime.strptime(follow_up_date, '%d/%m/%Y')
				follow_up_date = follow_up_date.strftime('%Y-%m-%d %H:%M:%S')

			enquiry = Enquiries(customer=customer, contact_name=contact_name, contact_number=contact_number, 
			contact_email=contact_email, site=site, site_number=site_number,follow_up_date=follow_up_date, 
			priority=priority, notes=notes, logged_by=logged_by, entered_date=entered_date)

			db.session.add(enquiry)
			db.session.commit()
			ncounter+=1
			flash('Enquiry added to database.')
			insertNotification(entered_date, logged_by, priority)
			return redirect('/')
		else:
			print form.errors
			flash('Error: All the form fields are required. ')
 
	return render_template('newEnquiryForm.html', form=form)

@app.route('/notifications')
@login_required
def notifications():
	global counter, ncounter
	counter = ncounter = 0
	# 10 most recent notifications
	data = Notifications.query.order_by(Notifications.datetime.desc()).limit(10)

	return render_template('notifications.html', data=data)


# # new estimate
# @app.route('/update')
# def update():
# 	id_number = request.args.get('id')
# 	# stage = request.args.get('stage')

# 	if not id_number:
# 		return redirect('orders')

# 	# if not stage:
# 		# return redirect('stages')

# 	form = updateForm()
# 	data = (db.session.query(Substages, Order_Substages).filter(Substages.id == Order_Substages.substage_id).filter(Order_Substages.order_id==id_number).all())
# 	# data = db.session.query(Substages).all()
# 	# print data

# 	dataDict = {}
# 	for row in data:
# 		dataDict[row[0].stage] = {}
# 	for row in data:
# 		dataDict[row[0].stage][row[0].substage] = row[1].data

# 	# using lists instead of dict
# 	# for row in data:
# 	# 	dataDict[row.stage] = []
# 	# for row in data:
# 	# 	dataDict[row.stage].append([row.substage,'x'])
			
# 	# print dataDict

# 	orderInfo = Orders.query.filter(Orders.id==id_number).all()

# 	return render_template('updateForm.html', form=form, data=dataDict, info=orderInfo)

# @app.route('/timeline')
# def timeline():
# 	id_number = request.args.get('id')

# 	if not id_number:
# 		return redirect('orders')

# 	substages = Substages.query.all()
# 	data = (db.session.query(Substages, Order_Substages).filter(Substages.id == Order_Substages.substage_id).filter(Order_Substages.order_id==id_number).all())
# 	orderInfo = Orders.query.filter(Orders.id==id_number).all()
# 	# print orderInfo[0].id
	
# 	resp = make_response(render_template('timeline.html', substages=substages, data=data, orderInfo=orderInfo[0]))
# 	resp.set_cookie('last', str(orderInfo[0].id))
# 	resp.set_cookie('refferer', 'timeline')
# 	return resp
# 	# return render_template('timeline.html', substages=substages, data=data, orderInfo=orderInfo[0])

from views import *

def insertNotification(datetime, logged_by, priority):
	notification = Notifications(datetime=datetime, logged_by=logged_by, priority=priority)
	db.session.add(notification)
	db.session.commit()

if __name__ == '__main__':
	#notifies in terminal when server has finished starting
	print 'Server Started Successfully'

	app.run(host='0.0.0.0', port=5001, threaded=True)
