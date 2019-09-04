from app.main import bp
from flask import render_template, flash, redirect


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Reparaturcafe Testseite',
                           user=user)
