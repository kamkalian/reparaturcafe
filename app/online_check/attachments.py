from app.online_check import bp
from flask_user import current_user, login_required
from flask import request, redirect, url_for, flash, current_app
from app.models import Attachment
import json
from werkzeug.utils import secure_filename
import os
from app import db


@bp.route('/attachment_list', methods=['POST'])
@login_required
def attachment_list():
    '''
    Lädt alle Anhänge zu einem Onlinecheck und gibt sie als Json Liste zurück.
    '''

    # ID aus den übermittelten POST Daten holen
    oc_id = request.form.get('oc_id')

    attachment_list = Attachment.query.filter_by(online_check_id=oc_id).all()
    attachment_filename_list = []
    for attachment in attachment_list:
        attachment_filename_list.append(attachment.filename)

    return json.dumps(attachment_filename_list)


def allowed_file(filename):
    '''
    Prüft ob der Dateiname einen Punkt enthält und ob die Endung erlaubt ist.
    '''
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/attachment_upload', methods=['POST'])
@login_required
def attachment_upload():
    '''
    Nimmt per POST eine hochgeladene Datei entgegen und speichert sie auf dem Server 
    im static/attachments Verzeichnis ab.
    Zusätzlich wird in der Datenbank ein Eintrag geschrieben.
    '''

    # ID aus den übermittelten POST Daten holen
    oc_id = request.form.get('oc_id')

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash(u'Fehler, Datei nicht gefunden!', 'danger')
            return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash(u'Bitte Datei auswählen!', 'danger')
            return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))