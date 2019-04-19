
from app.online_check import bp
from app.models import User
from flask_login import current_user, login_user, logout_user
from app.models import User, Role
from werkzeug.urls import url_parse
from flask_login import login_required
import json
from flask import render_template, redirect, flash
from app.onlinecheck.forms import NewOnlineCheckForm

@bp.route('/start_new_online_check', methods=['GET', 'POST'])
def start_new_online_check():
    form = NewOnlineCheckForm()
    #if form.validate_on_submit():
        #pass
    return render_template('online_check/new_online_check_form.html', title='1Online Check erstellen', form=form)

