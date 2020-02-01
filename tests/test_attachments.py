import pytest
from app.online_check import attachments
import json
from flask_user import current_user
from io import BytesIO, StringIO
from app.models import Onlinecheck, Attachment
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

    # OnlineCheck laden
    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    
    # Alle Anhämge durchlaufen
    for attachment in oc.attachments:

        # Für jedes Vorschaubild den Dateinamen ermitteln
        splitted_filename = attachment.filename.split('.')
        thumb_filename = str(attachment.id) + splitted_filename[0] + '_thumb.' + splitted_filename[1]

        # Dateiname aus ID und filename zusammenbauen
        converted_filename = str(attachment.id) + attachment.filename

        assert os.path.exists('app/static/attachments/' + converted_filename)
        assert os.path.exists('app/static/attachments/' + thumb_filename)
    
    filenames = [item.filename for item in oc.attachments]
    assert filename in filenames
    
    log_types = [item.type for item in oc.logs]
    assert 'attachment' in log_types




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
        assert [1, 'test.jpg'] in attachment_list

    if oc_id == 2:
        assert [2, 'test2.jpg'] in attachment_list
        assert [3, 'test3.jpg'] in attachment_list


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
def test_attachment_archive(app_logged_in, client, oc_id):
    '''
    Prüft ob sich die hochgeladenen Dateien inaktivieren lassen
    '''

    # Prüfen ob der redirect funktioniert
    assert client.post("/attachment_archive", data={'oc_id':oc_id}).status_code == 302

    response = client.post(
            '/attachment_archive',
            data = {
                'oc_id':oc_id,
                'attachment_id': '1'
            }
        )

    attachment = Attachment.query.filter_by(id=1).first()

    assert attachment.is_active is not True

    oc = Onlinecheck.query.filter_by(id=oc_id).first()
    log_types = [item.type for item in oc.logs]

    assert 'attachment' in log_types
    

@pytest.mark.parametrize(
    "attachment_id", [1, 2]
)
def test_attachment1(app_logged_in, client, attachment_id):
    '''
    Prüft ob der Anhang aufgerufen werden kann.
    '''
    
    assert client.get("/attachment/"+str(attachment_id)).status_code == 200