
from app.online_check import bp
from flask import render_template, redirect, flash, url_for
from app.online_check.forms import NewOnlineCheckForm

@bp.route('/start_new_online_check', methods=['GET', 'POST'])
def start_new_online_check():
    form = NewOnlineCheckForm()
    if form.validate_on_submit():
        flash('Neuer Online Check wurde erstellt.', 'success')
        return redirect(url_for('main.index'))
    return render_template('online_check/new_online_check_form.html', title='Online Check erstellen', form=form)

