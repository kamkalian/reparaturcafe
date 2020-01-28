from app.online_check import bp
from flask_user import current_user, login_required
from flask import request
from app.models import Attachment
import json


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


