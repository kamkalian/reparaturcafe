from datetime import datetime

from flask import json, url_for, request

from app import create_app, db
from app.config import TestConfig
import pytest
from app.models import Onlinecheck, Attachment, User
import flask_login


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():

        db.create_all()

        # mehrere Onlinechecks mit und ohne Anhänge erstellen
        oc = Onlinecheck(device_name='Leuchtturm', customer_name='Kurm')
        db.session.add(oc)
        db.session.commit()

        attachment = Attachment(online_check_id=oc.id, filename='test.jpg')
        db.session.add(attachment)

        oc = Onlinecheck(device_name='Mixer', customer_name='Kurm')
        db.session.add(oc)
        db.session.commit()
        attachment = Attachment(online_check_id=oc.id, filename='test2.jpg')
        db.session.add(attachment)
        attachment = Attachment(online_check_id=oc.id, filename='test3.jpg')
        db.session.add(attachment)

        oc = Onlinecheck(device_name='Toaster', customer_name='Kurm')
        db.session.add(oc)
        db.session.commit()

        # User Anlegen
        user = User(
            username="oskar",
            email="oskar@reparaturcafe.kurm.de",
            first_name="testus",
            last_name="tester",
            active=True,
            email_confirmed_at=datetime.now()
        )
        user.set_password("test")

        db.session.add(user)
        db.session.commit()

        yield app


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self):
        test_user = User.query.filter_by(username='oskar').first()
        flask_login.login_user(test_user)

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def app_logged_in(app, auth):
    auth.login()
    yield app