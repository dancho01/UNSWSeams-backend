import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1


def test1_clear_v1():
    clear_v1()  # Ensures that the datastruct is completely empty
    auth_register_v1('random123@gmail.com', '1234123', 'Bob', 'James')
    first_auth_id = int(auth_login_v1(
        "bob.smith@gmail.com", "comp1531")["auth_user_id"])
    valid_channel_id = int(channels_create_v1(
        first_auth_id, "first_channel", True)["channel_id"])
    assert(clear_v1() == {})
