import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.error import InputError, AccessError

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
def create_second_user():
    auth_user2_id = auth_register_v1('another_email@domain.com',
                                     'Password2', 'First', 'Last')['auth_user_id']
    return {'auth_user2_id': auth_user2_id}


@pytest.fixture
def create_first_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'first_new_channel_id': first_new_channel_id}


@pytest.fixture
def first_user_login():
    auth_user1_id = auth_login_v1(
        'valid_email@domain.com', 'Password1')["auth_user_id"]
    return {'auth_user1_id': auth_user1_id}


# creates user, verifies that the user is able to login, clears then login is attempted
# again but InputError should be raised as datastructure is empty.


def test1_clear_v1(create_first_user, first_user_login):
    '''
    Error raised:
        InputError: Checking if auth_user_id passed in is invalid.

    Explanation:
        Pytest fixture create_first_user is used to create the first user, assert ensures
        that you are able to login with that users details. The datastructure is then
        cleared and InputError is raised as the login details no longer reside within
        the data structure.
    '''
    assert(first_user_login['auth_user1_id'] ==
           create_first_user['auth_user1_id'])
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1("random123@gmail.com", "1234123")


def test2_clear_v1(create_first_channel_and_user, create_second_user):
    '''
    Error raised:
        AccessError: auth_user_id passed in is invalid

    Explanation:
        Pytest fixture create_first_channel_and_user returns auth_user1_id and
        first_channel_id after creating first user and first channel. Second user
        is then created and then it is cleared using clear_v1(). When trying to invite
        second user, AccessError wil be raised as the invitee does not exist.
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channel_invite_v1(
            create_first_channel_and_user['auth_user1_id'],
            create_first_channel_and_user['first_new_channel_id'], create_second_user)
