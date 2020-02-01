from app.online_check import bp
from flask_user import current_user, login_required
from flask import request, redirect, url_for, flash, current_app, render_template
from app.models import Attachment, Log
import json
from werkzeug.utils import secure_filename
import os
from app import db
from PIL import Image


@bp.route('/attachment/<attachment_id>', methods=['GET'])
@login_required
def attachment(attachment_id):
    '''
    Lädt ein Attachment und gibt das Template zurück.
    '''

    print(attachment_id)

    # Attachment laden
    attachment = Attachment.query.filter_by(id=attachment_id).first()

    return render_template('online_check/attachment.html',
                           title=attachment.online_check.device_name,
                           oc_id=attachment.online_check.id,
                           filename=attachment.filename,
                           attachment_id=attachment.id)




@bp.route('/attachment_list', methods=['POST'])
@login_required
def attachment_list():
    '''
    Lädt alle Anhänge zu einem Onlinecheck und gibt sie als Json Liste zurück.
    '''

    # ID aus den übermittelten POST Daten holen
    oc_id = request.form.get('oc_id')

    attachment_list = Attachment.query.filter_by(online_check_id=oc_id, is_active=1).all()
    attachment_filename_list = []
    for attachment in attachment_list:
        attachment_filename_list.append((attachment.id, attachment.filename))

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
        if file:

            if allowed_file(file.filename):
            
                # Datei speichern
                filename = secure_filename(file.filename)
                file.save('app/static/attachments/' + filename)

                # Bei Bildern ein Vorschaubild speichern
                splitted_filename = filename.split('.')
                thumb_filename = splitted_filename[0] + '_thumb.' + splitted_filename[1]
                try:
                    im = Image.open('app/static/attachments/' + filename)
                    im.thumbnail(current_app.config['THUMBNAIL_SIZE'])
                    im.save('app/static/attachments/' + thumb_filename)
                except Exception as e:
                    flash(u'Vorschaubild konnte nicht erstellt werden.', 'warning')

                # Eintrag in DB schreiben
                attachment = Attachment(online_check_id=oc_id, filename=filename)
                db.session.add(attachment)

                # Log Eintrag in DB schreiben
                if current_user.is_authenticated:
                    supervisor_id = current_user.id
                else:
                    supervisor_id = None
                log = Log(caption=filename,
                  online_check_id=oc_id,
                  user_id=supervisor_id,
                  type='attachment',
                  state='new')
                db.session.add(log)

                db.session.commit()

                flash(u'Datei wurde hochgeladen.', 'success')
                return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))
            
            else:
                extensions = ''
                for ext in current_app.config['ALLOWED_EXTENSIONS']:
                    extensions += ext + ', '
                flash(u'Es sind nur folgende Dateitypen erlaubt: ' + extensions[:-2], 'danger')
                return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))

    return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))


@bp.route('/attachment_archive', methods=['POST'])
@login_required
def attachment_archive():
    '''
    Archiviert einen Anhang, in dem bei dem Eintrag für den Anhang ein Flag gesetzt wird.
    '''

    # ID aus den übermittelten POST Daten holen
    oc_id = request.form.get('oc_id')
    attachment_id = request.form.get('attachment_id')

    if attachment_id:

        # Attachment laden
        attachment = Attachment.query.filter_by(id=attachment_id).first()
        attachment.is_active = False

        # Log Eintrag in DB schreiben
        if current_user.is_authenticated:
            supervisor_id = current_user.id
        else:
            supervisor_id = None
        log = Log(caption=attachment.filename,
            online_check_id=oc_id,
            user_id=supervisor_id,
            type='attachment',
            state='archived')
        db.session.add(log)

        db.session.commit()

        flash(u'Anhang ' + attachment.filename + ' wurde archiviert.', 'success')
        return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))

    else:

        flash(u'Anhang nicht gefunden', 'danger')
        return redirect(url_for('online_check.onlinecheck', oc_id=oc_id, new_comment=False))