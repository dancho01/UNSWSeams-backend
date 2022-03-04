import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

#channels_create_v1 tests
def test_0_invalid_channel_name_public():
    # tests for invalid channel name passed in 
    clear_v1()
    auth_reg_result = auth_register_v1(
        'randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_reg_result.get('auth_user_id')
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', True)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', True)

def test_invalid_channel_name_private():
    clear_v1()
    auth_reg_result = auth_register_v1(
        'randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_reg_result.get('auth_user_id')
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, '', False)
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'abcdefghijklmnopqrstuvwxyz', False)
        
def test_invalid_name_and_user_id():
    # when an invalid user id and channel name are passed in, an AccessError is thrown
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, '', True)
    with pytest.raises(AccessError):
        channels_create_v1(1, 'abcdefghijklmnopqrstuvwxyz', True)

def test_no_user_registered():
    # when no users are registered, any user id passed in is invalid
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, 'channelname', True)          

def test_correct_return_value():
    clear_v1()
    auth_reg_result = auth_register_v1(
        'randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_reg_result.get('auth_user_id')
    channels_result = channels_create_v1(auth_user_id, 'validname', True)
    channel_id = channels_result.get('channel_id')
    assert type(channel_id) is int
