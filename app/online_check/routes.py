import json
from app.online_check import bp
from flask import render_template, redirect, flash, url_for, request, session
from app.online_check.forms import NewOnlineCheckForm
from app.models import Onlinecheck, Log
from app import db
from flask_user import current_user, login_required
import datetime


@bp.route('/start_new_online_check', methods=['GET', 'POST'])
def start_new_online_check():
    form = NewOnlineCheckForm()
    if form.validate_on_submit():
        form = request.form.to_dict()
        if current_user.is_authenticated:
            supervisor_id = current_user.id
        else:
            supervisor_id = None
        oc = Onlinecheck(
            device_name=form['device_name'],
            device_issue=form['device_issue'],
            customer_name=form['customer_name'],
            customer_email=form['customer_email'],
            customer_tel=form['customer_tel'],
            supervisor_id=supervisor_id)
        db.session.add(oc)
        db.session.commit()

        log = Log(caption='Neu',
                  online_check_id=oc.id,
                  user_id=supervisor_id,
                  type='action',
                  state='Neu')
        db.session.add(log)
        db.session.commit()
        flash('Neuer Online Check wurde erstellt.', 'success')
        return redirect(url_for('main.index'))
    return render_template('online_check/new_online_check_form.html',
                           title='Online Check erstellen', form=form)


@bp.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():

    # State-Filter Session Variable
    state_filter_sess = session.get('state_filter')
    state_filter_get = request.args.get('state_filter')
    state_filter = 'all'
    if state_filter_get == 'all':
        session['state_filter'] = 'all'
    if state_filter_get == 'new':
        state_filter = 'new'
        session['state_filter'] = 'new'
    if state_filter_get is None:
        if state_filter_sess:
            state_filter = state_filter_sess

    # Vollbildmodus Session Variable
    light_sess = session.get('light')
    light_get = request.args.get('light')
    light = ''
    if light_get == 'go':
        light = '_light'
        session['light'] = '_light'
    if light_get == 'back':
        light = ''
        session['light'] = ''
    if light_get is None:
        if light_sess == '_light':
            light = '_light'

    oc_list = Onlinecheck.query.order_by(Onlinecheck.id.asc()).all()
    filtered_oc_list = []

    # letzten Status ermitteln und counter für den jeweiligen Status hochzählen
    c_all = 0
    c_new = 0
    for oc in oc_list:
        state = None
        state_caption = None
        thumbs = ''
        for log in oc.logs:
            if log.type == 'action':
                state = log.state
                state_caption = log.caption
                if state == "successfully":
                    thumbs = '_up'
                if state == "unsuccessfully":
                    thumbs = '_down'

        setattr(oc, 'state', state)
        setattr(oc, 'state_caption', state_caption)
        setattr(oc, 'thumbs', thumbs)

        date_diff = days_between(
            oc.logs[0].timestamp.strftime('%Y-%m-%d'),
            datetime.datetime.now().strftime('%Y-%m-%d'))
        setattr(oc, 'date_diff', date_diff)
        c_all += 1
        if state == 'new':
            c_new += 1
        if state == state_filter or state_filter == 'all':
            filtered_oc_list.append(oc)

    return render_template('online_check/overview.html', title='Übersicht',
                           oc_list=filtered_oc_list,
                           light=light,
                           c_all=c_all,
                           c_new=c_new,
                           state_filter=state_filter)

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


@bp.route('/onlinecheck/<oc_id>', methods=['GET', 'POST'])
@login_required
def onlinecheck(oc_id):
    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    logs = Log.query.filter_by(
        online_check_id=oc.id).order_by(Log.timestamp).all()
    return render_template('online_check/onlinecheck.html',
                           title=oc.device_name, oc=oc, logs=logs)


@bp.route('/get_new_ocs', methods=['GET', 'POST'])
@login_required
def get_new_ocs():
    oc_id_list = json.loads(request.form.get('oc_id_list'))
    oc_list = Onlinecheck.query.all()

    for oc in oc_list:

        if oc.id not in oc_id_list:
            oc = Onlinecheck.query.filter_by(id=oc.id).first()

            # letzten Status ermitteln
            state = None
            for log in oc.logs:
                if log.type == 'action':
                    state = log.caption

            # Supervisor ermitteln
            supervisor = ''
            if oc.user:
                supervisor = oc.user.username

            # Ersten Timestamp ermitteln
            timestamp = oc.logs[0].timestamp.strftime('%Y-%m-%d %I:%M:%S')

            return {'ok': 1,
                    'timestamp': timestamp,
                    'device_name': oc.device_name,
                    'oc_id': oc.id,
                    'customer_name': oc.customer_name,
                    'supervisor': supervisor,
                    'state': state}

    return {'ok': 0}


@bp.route('/get_c_new', methods=['GET', 'POST'])
@login_required
def get_c_new():
    oc_list = Onlinecheck.query.order_by(Onlinecheck.id.asc()).all()

    # letzten Status ermitteln und counter für den jeweiligen Status hochzählen
    c_new = 0
    for oc in oc_list:
        state = None
        for log in oc.logs:
            if log.type == 'action':
                state = log.state
        if state == 'new':
            c_new += 1

    return {'c_new': c_new}
