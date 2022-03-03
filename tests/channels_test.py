import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

auth_reg_result = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
auth_reg_result = auth_register_v1('secrandomuser@gmail.com', 'password', 'Jin', 'Cho')    
auth_reg_result = auth_register_v1('thirdrandomuser@gmail.com', 'password', 'Jen', 'Cho')        
auth_user_id = auth_reg_result.get('auth_user_id') 
channels_result = channels_create_v1(auth_user_id, 'validname', True)
channel_id = channels_result.get('channel_id')

def test_0_invalid_channel_name_public():
    clear_v1()
    auth_reg_result = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_reg_result.get('auth_user_id')
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', True)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', True)

def test_1_invalid_channel_name_private():
    clear_v1()
    auth_reg_result = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_reg_result.get('auth_user_id') 
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', False)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', False)

def test_2_invalid_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, 'randomename', True)
        
def test_3_correct_return_value():
    clear_v1()
    auth_reg_result = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')    
    auth_user_id = auth_reg_result.get('auth_user_id') 
    channels_result = channels_create_v1(auth_user_id, 'validname', True)
    channel_id = channels_result.get('channel_id')
    assert type(channel_id) is int
    
    
