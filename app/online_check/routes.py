
from app.online_check import bp
from flask import render_template, redirect, flash, url_for, request
from app.online_check.forms import NewOnlineCheckForm
from app.models import Onlinecheck, Log
from app import db
from flask_user import current_user, login_required


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

        log = Log(caption='Onlinecheck gestartet',
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
    oc_list = Onlinecheck.query.all()
    return render_template('online_check/overview.html', title='Übersicht',
                           oc_list=oc_list)


@bp.route('/onlinecheck/<oc_id>', methods=['GET', 'POST'])
@login_required
def onlinecheck(oc_id):
    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    logs = Log.query.filter_by(
        online_check_id=oc.id).order_by(Log.timestamp).all()
    return render_template('online_check/onlinecheck.html',
                           title=oc.device_name, oc=oc, logs=logs)
