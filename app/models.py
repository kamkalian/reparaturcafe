from app import db
from datetime import datetime
from flask_user import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')

    email = db.Column(db.String(255),
                      nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100),
                           nullable=False, server_default='')
    last_name = db.Column(
        db.String(100), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    online_checks = db.relationship('Onlinecheck', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Role(db.Model):
    __tablemame__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(64), index=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))


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
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    logs = db.relationship('Log', backref='online_check')


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    online_check_id = db.Column(db.Integer, db.ForeignKey('online_check.id'))
    caption = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
