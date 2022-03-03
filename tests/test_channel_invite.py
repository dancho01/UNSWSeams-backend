import pytest

from src.error import InputError
from src.error import AccessError
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.data_store import checkValidChannel, checkAuthorization, messagesReturned, data_store

def test_invalid_channel_id():
    clear_v1()
    auth_user_id = auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")
    new_user_id = auth_register_v1("another_email@domain.com", "Password2", "First", "Last")

    with pytest.raises(InputError): # should raise an exception
        channel_invite_v1(auth_user_id, 3, new_user_id)     # assume channel_id 3 does not exist

def test_invalid_u_id():
    clear_v1()
    auth_user_id = auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")
    new_channel = channels_create_v1(auth_user_id, "Channel Name", True)

    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, new_channel, 3)    # assume u_id 3 does not exist

def test_already_channel_member():
    # tests that u_id is already in the channel
    
    clear_v1()
    u_id1 = auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")
    u_id2 = auth_register_v1("another_email@domain.com", "Password2", "First", "Last")
    channel1 = channels_create_v1(u_id1, "Channel Name", True)   # returns an integer channel_id
    channel_join_v1(u_id2, channel1)

    with pytest.raises(InputError):
        channel_invite_v1(u_id1, channel1, u_id2)
    
def test_auth_user_not_in_channel():
    # test both users not in channel
    clear_v1()
    u_id1 = auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")
    u_id2 = auth_register_v1("another_email@domain.com", "Password2", "First", "Last")
    u_id3 = auth_register_v1("third_email@domain.com", "Password3", "First", "Last")

    channel1 = channels_create_v1(u_id3, "Channel Name", True).get("id")   # returns channel_id
    print(channel1)
    with pytest.raises(AccessError):
        channel_invite_v1(u_id1, channel1, u_id2)

def test_invalid_auth_user_id():
    # when auth_user_id does not exist
    clear_v1()
    u_id2 = auth_register_v1("another_email@domain.com", "Password2", "First", "Last")
    u_id3 = auth_register_v1("third_email@domain.com", "Password3", "First", "Last")
    channel1 = channels_create_v1(u_id2, "Channel Name", True)   # returns an integer channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(1, channel1, u_id3)   # assumes 1 is not a valid user_id