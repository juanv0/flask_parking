from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time
from app import app

class User(UserMixin, db.Model):
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(300), index=True, unique=True)
		email = db.Column(db.String(300), index=True, unique=True)
		password_hash = db.Column(db.String(300))
		name = db.Column(db.String(300), index =True)
		
		def set_password(self, password):
			self.password_hash = generate_password_hash(password)
			
		def check_password(self, password):
			return check_password_hash(self.password_hash, password)
		
		def get_reset_password_token(self, expires_in=1800):
			return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode(utf-8)
			
		@staticmethod
		def verify_reset_password_token(token):
			try:
				id = jwt.decode(token, app.config['client_secret'], algorithms=['HS256'])['reset_password']
			except:
				return
			return User.query.get(id)

			
@login.user_loader
def load_user(id):
	return User.query.get(int(id))