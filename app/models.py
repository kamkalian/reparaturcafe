from app import db, login
from sqlalchemy import func, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


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


class Onlinecheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(128))
    device_issue = db.Column(db.String(1000))
    device_opened = db.Column(db.Boolean)
    device_manual = db.Column(db.Boolean)
    customer_name = db.Column(db.String(128))
    customer_email = db.Column(db.String(128))
    customer_tel = db.Column(db.String(128))


