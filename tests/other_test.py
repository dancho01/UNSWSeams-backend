import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.data_store import data_store


def test1_clear_v1():
    clear_v1()  # Ensures that the datastruct is completely empty
    auth_register_v1('random123@gmail.com', '1234123', 'Bob', 'James')
    first_auth_id = int(auth_login_v1(
        "random123@gmail.com", "1234123")["auth_user_id"])
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1("random123@gmail.com", "1234123")


# def test2_clear_v1():
#     clear_v1()  # Ensures that the datastruct is completely empty
#     auth_register_v1('random123@gmail.com', '1234123', 'Bob', 'James')
#     first_auth_id = int(auth_login_v1(
#         "random123@gmail.com", "1234123")["auth_user_id"])
#     first_channel_id = channels_create_v1(first_auth_id, "New channel", True)
#     clear_v1()

#     with pytest.raises(InputError):
#         auth_login_v1("random123@gmail.com", "1234123")
