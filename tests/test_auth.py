from flask import session
from flask_user import current_user

from app.models import User
import pytest


def test_login_n_out(client, auth):
    assert client.get("/auth/login").status_code == 200
    auth.login()
    assert current_user.is_authenticated is True
    auth.logout()
    assert "client" not in session
    assert current_user.is_authenticated is False