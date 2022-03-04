import pytest

from src.error import InputError
from src.error import AccessError
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.data_store import check_valid_channel, check_authorization, messages_returned, data_store, check_user_registered

def test_invalid_auth_user_id():
    # when auth_user_id does not exist
    clear_v1()
    u_id2 = int(auth_register_v1("another_email@domain.com", "Password2", "First", "Last")["auth_user_id"])
    u_id3 = int(auth_register_v1("third_email@domain.com", "Password3", "First", "Last")["auth_user_id"])
    channel1 = int(channels_create_v1(u_id2, "Channel Name", True)["channel_id"])   # returns an integer channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(1, channel1, u_id3)   # assumes 1 is not a valid user_id
