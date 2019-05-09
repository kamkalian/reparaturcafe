from app.main import bp
from flask import render_template, flash, redirect
from app.forms import LoginForm
from app.models import FFPing
from app import db
import json


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Reparaturcafe Testseite', user=user)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Du bist nun eingeloggt.', 'success')
        return redirect('/index')
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/ff_router_stat')
def ff_router_stat():

    return redirect('/ff_router_stat')


@bp.route('/ff_router_sign_of_life/<response_time>')
def ff_router_sign_of_life(response_time):
    ffping = FFPing(response_time=response_time)
    db.session.add(ffping)
    db.session.commit()
    return '''True'''


