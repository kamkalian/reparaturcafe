import pytest
from app.online_check import attachments
import json
from flask_user import current_user

@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
def test_attachment_list(auth, client, oc_id):
 
    auth.login()

    assert client.post("/attachment_list").status_code == 200
    attachment_list_json = client.post("/attachment_list", data={'oc_id':oc_id})
    
    attachment_list = json.loads(attachment_list_json.data)    

    assert len(attachment_list) > 0


@pytest.mark.parametrize(
    "oc_id", [3]
)
def test_empty_attachment_list(auth, oc_id):  

    auth.login() 
    
    attachment_list_json = attachments.attachment_list(oc_id)
    attachment_list = json.loads(attachment_list_json)

    assert len(attachment_list) == 0