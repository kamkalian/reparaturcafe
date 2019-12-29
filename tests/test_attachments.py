import pytest
from app.online_check import attachments


@pytest.mark.parametrize(
    "oc_id", [1, 2]
)
def test_attachment_list(app, auth, oc_id):
 
    auth.login()

    attachment_list = attachments.attachment_list(oc_id)

    assert len(attachment_list) > 0


@pytest.mark.parametrize(
    "oc_id", [3]
)
def test_empty_attachment_list(auth, oc_id):  

    auth.login() 
    
    attachment_list = attachments.attachment_list(oc_id)

    assert len(attachment_list) == 0