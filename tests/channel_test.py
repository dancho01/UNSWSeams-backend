import pytest
from src.error import InputError, AccessError
from src.channel import channel_messages_v1, channel_details_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1

# tests for channel_details_v1


def test_invalid_channel():
    clear_v1()
    auth_register_v1("bob.smith@gmail.com", "comp1531", "Bob", "Smith")
    first_auth_id = int(auth_login_v1(
        "bob.smith@gmail.com", "comp1531").get("auth_user_id"))
    valid_channel_id = int(channels_create_v1(
        first_auth_id, "first_channel", True)["channel_id"])
    with pytest.raises(InputError):
        channel_details_v1(first_auth_id, valid_channel_id + 1)


def test_invalid_user():
    clear_v1()
    auth_register_v1("bob.smith@gmail.com", "comp1531", "Bob", "Smith")
    first_auth_id = int(auth_login_v1(
        "bob.smith@gmail.com", "comp1531").get("auth_user_id"))
    valid_channel_id = int(channels_create_v1(
        first_auth_id, "first_channel", True)["channel_id"])
    with pytest.raises(AccessError):
        channel_details_v1(first_auth_id + 1, valid_channel_id)


# tests for channel_messages_v1

def invalid_start_index():
    clear_v1()
    auth_register_v1("bob.smith@gmail.com", "comp1531", "Bob", "Smith")
    first_auth_id = int(auth_login_v1(
        "bob.jane@gmail.com", "comp1531").get("auth_user_id"))
