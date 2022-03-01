import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1
 
def test_0_invalid_channel_name_public():
    clear_v1()
    auth_user_id = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', True)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', True)

def test_1_invalid_channel_name_private():
    clear_v1()
    auth_user_id = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')   
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', False)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', False)

