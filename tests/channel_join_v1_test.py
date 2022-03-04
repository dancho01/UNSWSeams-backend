import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_0_invalid_channel_id():
    clear_v1()
    auth_register_return = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_register_return.get('auth_user_id')
    # InputError as user is trying to join a channel that does not yet exist
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id, 1)
    
def test_1_auth_user_already_member():
    clear_v1()
    auth_register_return = auth_register_v1('randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_register_return.get('auth_user_id')    
    channels_result = channels_create_v1(auth_user_id, 'validname', True)
    channel_id = channels_result.get('channel_id')
    # InputError is thrown as authorised user is already a channel member
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id, channel_id)

def test_2_join_priv_channel():
    clear_v1()
    auth_register_return = auth_register_v1('firstuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id_1 = auth_register_return.get('auth_user_id')    
    # user 1 (global owner) creates a private channel, making him channel owner/member
    channels_result = channels_create_v1(auth_user_id_1, 'validname', False)
    channel_id = channels_result.get('channel_id')
    # user 2 is registered (not a global owner)
    auth_register_return = auth_register_v1('seconduser@gmail.com', 'password', 'firstname', 'lastname')
    auth_user_id_2 = auth_register_return.get('auth_user_id')    
    with pytest.raises(AccessError):
        channel_join_v1(auth_user_id_2, channel_id)
    # AccessError is thrown as user 2, who is not channel member/global owner, tries to join private channel
    
def test_3_invalid_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channel_join_v1(1, 1)  
        
def test_4_correct_return_type():
    clear_v1()
    auth_register_return = auth_register_v1('firstuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id_1 = auth_register_return.get('auth_user_id')  
    channels_result = channels_create_v1(auth_user_id_1, 'validname', True)
    channel_id = channels_result.get('channel_id')
    auth_register_return = auth_register_v1('seconduser@gmail.com', 'password', 'firstname', 'lastname')
    auth_user_id_2 = auth_register_return.get('auth_user_id')  
    # success case        
    assert channel_join_v1(auth_user_id_2, channel_id) == {}   

  
        
   
