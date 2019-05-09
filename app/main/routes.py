from app.main import bp
from flask import render_template, flash, redirect
from app.forms import LoginForm


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
