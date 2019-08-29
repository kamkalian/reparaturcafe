import os
import hashlib


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    password = os.environ.get("MYSQL_PASSWORD")
    username = os.environ.get("MYSQL_USER")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://' + username + ':' + password + '@localhost/reparaturcafe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
