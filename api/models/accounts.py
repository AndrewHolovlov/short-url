from . import db

from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    fist_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    password = db.Column(db.String)

    def __init__(self, email, fist_name, last_name, password):
        self.email = email
        self.fist_name = fist_name
        self.last_name = last_name
        self.password = password
        self.hash_password()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


