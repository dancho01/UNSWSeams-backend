import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.data_store import data_store, check_user_registered

'''
Pytest fixtures
'''


@pytest.fixture
def create_first_user():
    clear_v1()
    auth_user1_id = auth_register_v1(
        'valid_email@domain.com', 'Password1', 'First', 'Last')['auth_user_id']
    return {'auth_user1_id': auth_user1_id}


@pytest.fixture
def create_first_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'first_new_channel_id': first_new_channel_id}


@pytest.fixture
def create_second_user():
    auth_user2_id = auth_register_v1('another_email@domain.com',
                                     'Password2', 'First', 'Last')['auth_user_id']
    return {'auth_user2_id': auth_user2_id}


def test1_clear_v1():
    clear_v1()  # Ensures that the datastruct is completely empty
    auth_register_v1('random123@gmail.com', '1234123', 'Bob', 'James')
    first_auth_id = int(auth_login_v1(
        "random123@gmail.com", "1234123")["auth_user_id"])
    assert(auth_login_v1("random123@gmail.com", "1234123")
           ['auth_user_id'] == first_auth_id)
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
