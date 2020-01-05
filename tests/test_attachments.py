import pytest
from app.online_check import attachments
import json


@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
def test_attachment_list(app, auth, client, oc_id):
 
    auth.login()

    data = {'oc_id':oc_id}
    attachment_list_json = client.post('/attachment_list', data=json.dumps(data))
    print(attachment_list_json.json)
    attachment_list = json.loads(attachment_list_json.json)    

    assert len(attachment_list) > 0


@pytest.mark.parametrize(
    "oc_id", [3]
)
def test_empty_attachment_list(auth, oc_id):  

    auth.login() 
    
    attachment_list_json = attachments.attachment_list(oc_id)
    attachment_list = json.loads(attachment_list_json)

    assert len(attachment_list) == 0