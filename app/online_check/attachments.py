from app.online_check import bp
from flask_user import current_user, login_required
from app.models import Attachment


@bp.route('/attachment_list/oc_id', methods=['POST'])
@login_required
def attachment_list(oc_id):
    '''
    Lädt alle Anhänge zu einem Onlinecheck und gibt sie als Liste zurück.
    '''

    attachment_list = Attachment.query.filter_by(online_check_id=oc_id).all()

    return attachment_list
