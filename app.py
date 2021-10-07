import os

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

skill_list = [
	"Python", 
	"JavaScript", 
	"SQL", 
	"HTML/CSS", 
	"Heroku",
	"DigitalOcean",
	"CloudFlare",
	"Linux",
	"MacOS",
	"Windows",
	"Raspberry Pi"
	"Arduino",
	"Ergonomic Design",
	"Process Engineering",
	"FMEA/DFMEA", 
	"Facility Layout", 
	"SolidWorks", 
	"AutoCAD", 
	"Microsoft Office", 
	"Oscilloscope", 
	"Digital Multimeter", 
	"Soldering",
	"Biomedical Sciences",
	"French",
	"Home Improvement",
	"Guitar Playing",
	"Guitar Making",
	"Piano",
	"Cooking",
	"Forklift",
	"Scissor Lift",
	"ISO", 
	"UL/ETL"
]

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'here have a secret key'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class Role(db.Model):
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name= db.Column(db.String(64), unique=True)

	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename='users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)

	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


class NameForm(FlaskForm):
	name = StringField("What's your name?", validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


@app.route('/education', methods=['GET', 'POST'])
def education():
	return render_template('education.html')

@app.route('/employment', methods=['GET', 'POST'])
def employment():
	return render_template('employment.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
	return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	return render_template('contact.html')

@app.route('/skills', methods=['GET', 'POST'])
def skills():
	return render_template('skills.html', skills=skill_list)
