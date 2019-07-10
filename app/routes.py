from flask import render_template, redirect, flash, url_for, request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import current_user, login_required, logout_user, login_user
from app import app, db
from app.email import send_password_reset_email


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
	return render_template('index.html', title='Hello')
	
	
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash ("Felicidades ya estas Registrado en la base de datos")
		return redirect(url_for('login'))
	return render_template('registrar.html', title='Registrarse', form=form)
	
	
@app.route("/loguear",  methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Nombre de usuario o contraseña invalida")
			return redirect(url_for('login'))
		login_user(user, remember=True)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('loguear.html', title='Ingresar', form=form)
	
	
@app.route("/salir")
def logout():
	logout_user()
	return redirect(url_for('index'))
	
	
@app.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Revise su correo electronico y siga las instrucciones para Reestablecer su contraseña')
		return redirect(url_for('index'))
	return render_template('reset_password_request.html', tilte='Reestablecer Password', form=form)
	
	
@app.route("/reset_password/<token>")
def reset_password():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Su contraseña ha sido reestablecida')
		return redirect(url_for('index'))
	return render_template('reset_password.html', form=form)
	
	

@app.route("/camera")
@login_required
def camera():
	return render_template('camera.html')
			
		