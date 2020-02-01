import pytest
from app.online_check import attachments
import json
from flask_user import current_user
from io import BytesIO, StringIO
from app.models import Onlinecheck
import os.path
from PIL import Image


@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
@pytest.mark.parametrize(
    "filename", ['test1.png', 'test2.jpg']
)
def test_attachment_upload(auth, client, oc_id, filename):
    '''
    Prüft ob der Datei Upload funktioniert.
    '''
 
    # Testuser einloggen
    auth.login()

    # Prüfen ob der redirect funktioniert
    assert client.post("/attachment_upload", data={'oc_id':oc_id}).status_code == 302

    # Eine Bild-Datei im Speicher erstellen
    f = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(f, 'png')
    f.name = filename
    f.seek(0)

    response = client.post(
            '/attachment_upload',
            data = {
                'oc_id':oc_id,
                'file': (f, f.name),
            }
        )

    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    filenames = [item.filename for item in oc.attachments]
    log_types = [item.type for item in oc.logs]

    splitted_filename = filename.split('.')
    thumb_filename = splitted_filename[0] + '_thumb.' + splitted_filename[1]
    
    assert filename in filenames
    assert os.path.exists('app/static/attachments/' + filename)
    assert os.path.exists('app/static/attachments/' + thumb_filename)
    assert 'upload' in log_types


@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
def test_attachment_list(auth, client, oc_id):
 
    auth.login()

    assert client.post("/attachment_list").status_code == 200
    attachment_list_json = client.post("/attachment_list", data={'oc_id':oc_id})
    
    attachment_list = json.loads(attachment_list_json.data)    

    assert len(attachment_list) > 0
    
    if oc_id == 1:
        assert 'test.jpg' in attachment_list

    if oc_id == 2:
        assert 'test2.jpg' in attachment_list
        assert 'test3.jpg' in attachment_list


@pytest.mark.parametrize(
    "oc_id", [3]
)
def test_empty_attachment_list(auth, client, oc_id):  

    auth.login() 
    
    attachment_list_json = client.post("/attachment_list", data={'oc_id':oc_id})
    attachment_list = json.loads(attachment_list_json.data)

    assert len(attachment_list) == 0


@pytest.mark.parametrize(
    "filename", ['test1.png', 'test2.jpg', 'test3.pdf']
)
def test_allowed_extensions(auth, client, filename):
    '''
    Prüfen ob bestimmte Dateieendungen erlaubt sind.
    '''

    assert attachments.allowed_file(filename)


@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
@pytest.mark.parametrize(
    "filename", ['test1.png', 'test2.jpg']
)
def test_attachment_inactive(app_logged_in, oc_id, filename):
    '''
    Prüft ob sich die hochgeladenen Dateien inaktivieren lassen
    '''

    # Prüfen ob der redirect funktioniert
    assert client.post("/attachment_inactive", data={'oc_id':oc_id}).status_code == 302