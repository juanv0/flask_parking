from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
	name = StringField("Nombre Completo", validators=[DataRequired()])
	username = StringField("Nombre de Usuario", validators=[DataRequired()])
	password = PasswordField("Contraseña", validators=[DataRequired()])
	password2 = PasswordField("Confirmar Contraseña", validators=[DataRequired(), EqualTo("password")])
	email = StringField("Correo Electronico", validators=[DataRequired(), Email()])
	submit = SubmitField("Enviar")
	
	@staticmethod
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError("Nombre de Usuario ya registrado, por favor ingrese otro")
			
	@staticmethod
	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError("Correo Electronico ya registrado, por favor ingrese otro")
			
			
class LoginForm(FlaskForm):
	username = StringField("Nombre de usuario", validators=[DataRequired()])
	password = PasswordField("Contraseña", validators=[DataRequired()])
	submit = SubmitField("Ingresar")
	

class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Correo Electronico', validators=[DataRequired()])
	submit = SubmitField('Enviar')
	
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Contraseña', validators=[DataRequired()])
	password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Enviar')