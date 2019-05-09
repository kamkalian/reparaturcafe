
from app.online_check import bp
from flask import render_template, redirect, flash, url_for, request
from app.online_check.forms import NewOnlineCheckForm
from app.models import Onlinecheck, Log
from app import db

@bp.route('/start_new_online_check', methods=['GET', 'POST'])
def start_new_online_check():
    form = NewOnlineCheckForm()
    if form.validate_on_submit():
        form = request.form.to_dict()
        print(form)
        oc = Onlinecheck(
            device_name=form['device_name'],
            device_issue=form['device_issue'],
            customer_name=form['customer_name'],
            customer_email=form['customer_email'],
            customer_tel=form['customer_tel'])
        db.session.add(oc)
        db.session.commit()

        log = Log(caption='Onlinecheck gestartet', online_check_id=oc.id)
        db.session.add(log)
        db.session.commit()
        flash('Neuer Online Check wurde erstellt.', 'success')
        return redirect(url_for('main.index'))
    return render_template('online_check/new_online_check_form.html', title='Online Check erstellen', form=form)

@bp.route('/overview', methods=['GET', 'POST'])
def overview():
    oc_list = Onlinecheck.query.all()
    return render_template('online_check/overview.html', title='Übersicht', oc_list=oc_list)


@bp.route('/show/<oc_id>', methods=['GET', 'POST'])
def show(oc_id):
    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    return render_template('online_check/show.html', title=oc.device_name, oc=oc)