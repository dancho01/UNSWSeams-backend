import pytest

from src.error import InputError
from src.error import AccessError
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.data_store import check_valid_channel, check_authorization, messages_returned, data_store, check_user_registered


def test_invalid_channel_id():
    clear_v1()
    auth_user_id = int(auth_register_v1(
        "valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    new_user_id = int(auth_register_v1("another_email@domain.com",
                      "Password2", "First", "Last")["auth_user_id"])
    new_channel = int(channels_create_v1(
        auth_user_id, "Channel Name", True)["channel_id"])

    with pytest.raises(InputError):  # should raise an exception
        channel_invite_v1(auth_user_id, new_channel + 1, new_user_id)


def test_invalid_u_id():
    clear_v1()
    auth_user_id = int(auth_register_v1(
        "valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    new_channel = int(channels_create_v1(
        auth_user_id, "Channel Name", True)["channel_id"])

    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, new_channel, auth_user_id + 1)    # assume u_id 3 does not exist

def test_already_channel_member():
    # tests that u_id is already in the channel

    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com",
                "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com",
                "Password2", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True)[
                   "channel_id"])   # returns an integer channel_id
    channel_join_v1(u_id2, channel1)

    with pytest.raises(InputError):
        channel_invite_v1(u_id1, channel1, u_id2)


def test_auth_user_not_in_channel():
    # test both users not in channel and channel_id is valid
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com",
                "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com",
                "Password2", "First", "Last")["auth_user_id"])
    u_id3 = int(auth_register_v1("third_email@domain.com",
                "Password3", "First", "Last")["auth_user_id"])

    channel1 = int(channels_create_v1(u_id3, "Channel Name",
                   True).get("channel_id"))   # returns channel_id
    with pytest.raises(AccessError):
        channel_invite_v1(u_id1, channel1, u_id2)


def test_invalid_auth_user_id():
    # when auth_user_id does not exist
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True)[
                   "channel_id"])   # returns an integer channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id2 + 1, channel1, u_id2)

    # test multiple errors
def test_all_input_errors():
    # all three input errors
    # so auth user not in channel, and channel is invalid, u_id invalid
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])

    channel1 = int(channels_create_v1(u_id2, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(InputError): 
        channel_invite_v1(u_id1, channel1 + 1, u_id2 + 1)

    # test 1 access 1 input error
def test_invalid_auth_invalid_channel():
    # test auth_user_id doesn't exist & invalid channel
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(AccessError): 
        channel_invite_v1(u_id2 + 1, channel1 + 1, u_id2)

    # test 1 access 1 input error
def test_invalid_auth_invalid_u_id():
    # test auth_user_id doesn't exist & invalid u_id
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(AccessError): 
        channel_invite_v1(u_id1 + 1, channel1, u_id1 + 2)

    # test 1 access 1 input error
def test_invalid_auth_id_inviting_existing_member():
    # test auth_user_id doesn't exist & u_id already a member
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(AccessError): 
        channel_invite_v1(u_id1 + 1, channel1, u_id1)

    # test 1 access 1 input error
def test_unauthorised_auth_id_inviting_non_registered_user():
    # test auth_user_id not a member of channel & invalid u_id
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(AccessError): 
        channel_invite_v1(u_id2, channel1, u_id2 + 1)

    # test 1 access 1 input error
def test_unauthorised_auth_id_inviting_existing_channel_member():
    # test auth_user_id not a member of channel & invalid u_id
    clear_v1()
    u_id1 = int(auth_register_v1("valid_email@domain.com", "Password1", "First", "Last")["auth_user_id"])
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id1, "Channel Name", True).get("channel_id"))   # returns channel_id

    with pytest.raises(AccessError): 
        channel_invite_v1(u_id2, channel1, u_id1)
    
    # test both input and access errors - access errors should be called first

    # test all 5 errors


# test 
    # edges cases
    # no users

    # one user

    # multiple users
