import json
from app.online_check import bp
from app.online_check.state_structure import get_posible_states
from flask import render_template, redirect, flash, url_for, request, session, jsonify
from app.online_check.forms import NewOnlineCheckForm
from app.models import Onlinecheck, Log
from app import db
from flask_user import current_user, login_required
import datetime
from app.oskar_bot.bot import send_message
from app.config import Config

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
                  state='new')
        db.session.add(log)
        db.session.commit()
        text = 'Ein neuer Onlinecheck wurde erstellt: *' + oc.device_name + '* \n https://q01.reparaturcafe.online/onlinecheck/' + str(oc.id)
        send_message(str(Config.TELEGRAM_CHAT_ID), text=text, parse_mode='Markdown')
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

    # oc_list = Onlinecheck.query.join(Onlinecheck.logs).filter(not_(Log.state=='closed')).order_by(Onlinecheck.id.asc()).all()
    oc_list = Onlinecheck.query.filter(
        ~Onlinecheck.logs.any(Log.state=='closed')
    ).all()
    filtered_oc_list = []

    # letzten Status ermitteln und counter für den jeweiligen Status hochzählen
    c_all = 0
    c_new = 0
    for oc in oc_list:
        oc, state = state_check(oc)
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


def state_check(oc):
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
    return oc, state


@bp.route('/onlinecheck/<oc_id>', methods=['GET', 'POST'])
@login_required
def onlinecheck(oc_id):
    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    logs = Log.query.filter_by(
        online_check_id=oc.id).order_by(Log.timestamp).all()

    oc, state = state_check(oc) # letzten Status+Caption ermitteln und Zeitraum ausrechnen und dem onlinecheck hinzufügen.
    posible_states = get_posible_states(state) # anhand des aktuelles Status werden nun alle möglichen Status ermittelt.

    if current_user.is_authenticated:
        supervisor_id = current_user.id
    else:
        supervisor_id = None

    # Wenn ein POST gesendet wurde wird ein neuer Kommentar angelegt.
    if request.method == 'POST':
        
        if 'new_comment_form' in request.form:
            comment = request.form.get('comment')
            log = Log(caption=comment,
                    online_check_id=oc.id,
                    user_id=supervisor_id,
                    type='comment')
            db.session.add(log)
            db.session.commit()

        return redirect(url_for('online_check.onlinecheck', oc_id=oc.id, new_comment=True))

    if request.args.get('new_comment'):
        return render_template('online_check/onlinecheck.html', _anchor='new_comment',
                               title=oc.device_name, oc=oc, logs=logs, posible_states=posible_states)

    return render_template('online_check/onlinecheck.html',
                           title=oc.device_name, oc=oc, logs=logs, posible_states=posible_states)


@bp.route('/get_new_ocs', methods=['GET', 'POST'])
@login_required
def get_new_ocs():
    oc_id_list = json.loads(request.form.get('oc_id_list'))
    oc_list = Onlinecheck.query.filter(
        ~Onlinecheck.logs.any(Log.state=='closed')
    ).all()

    state_filter_sess = session.get('state_filter')


    for oc in oc_list:

        if oc.id not in oc_id_list:
            oc = Onlinecheck.query.filter_by(id=oc.id).first()

            # letzten Status ermitteln
            state = None
            state_caption = None
            for log in oc.logs:
                if log.type == 'action':
                    state_caption = log.caption
                    state = log.state
            
            if state != state_filter_sess:
                continue            

            # Supervisor ermitteln
            supervisor = ''
            if oc.user:
                supervisor = oc.user.username

            # Ersten Timestamp ermitteln
            timestamp = oc.logs[0].timestamp.strftime('%Y-%m-%d %I:%M:%S')

            return jsonify({'ok': 1,
                    'timestamp': timestamp,
                    'device_name': oc.device_name,
                    'oc_id': oc.id,
                    'customer_name': oc.customer_name,
                    'supervisor': supervisor,
                    'state': state_caption})

    return jsonify({'ok':0})


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
    return jsonify({'c_new': c_new})


@bp.route('/change_state/<oc_id>', methods=['GET', 'POST'])
@login_required
def change_state(oc_id):
    # print(request.form.get('new_state'))
    new_state = request.form.get('new_state')
    new_state_caption = request.form.get('new_state_caption')

    supervisor_id = current_user.id

    # TODO überprüfen ob der Statuswechseln erlaubt ist
    # posible_states = get_posible_states(new_state)

    log = Log(caption=new_state_caption,
                  online_check_id=oc_id,
                  user_id=supervisor_id,
                  type='action',
                  state=new_state)
    db.session.add(log)
    db.session.commit()
    flash('Status wurde geändert.', 'success')

    return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))

