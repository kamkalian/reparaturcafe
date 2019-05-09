from app import db, login
from sqlalchemy import func, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from hashlib import md5
from time import time
import jwt
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    __tablemame__ = 'role'
    name = db.Column(db.String(64), primary_key=True)
    desc = db.Column(db.String(64), index=True)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    lastname = db.Column(db.String(50), index=True)
    firstname = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), db.ForeignKey('role.name'))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Onlinecheck(db.Model):
    __tablename__ = 'online_check'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(128))
    device_issue = db.Column(db.String(1000))
    device_opened = db.Column(db.Boolean)
    device_manual = db.Column(db.Boolean)
    customer_name = db.Column(db.String(128))
    customer_email = db.Column(db.String(128))
    customer_tel = db.Column(db.String(128))
    logs = db.relationship('Log', backref='online_check')


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    online_check_id = db.Column(db.Integer, db.ForeignKey('online_check.id'))
    caption = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class FFPing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_time = db.Column(db.Float())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

