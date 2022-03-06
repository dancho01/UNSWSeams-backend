import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.other import clear_v1

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

# Test for channels_list_v1


# Testing if all public channels in server linked to the individual
def test_0_one_user_multiple_public_channels():
    # users is able to be messaged.
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    channels_create_v1(first_id, 'First', True)
    channels_create_v1(first_id, "Second", True)
    assert(channels_list_v1(first_id) != {})


# Testing if all channels, public and private, linked to the individual
def test_1_one_user_multiple_mixed_channels():
    # user is listed.
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    channels_create_v1(first_id, 'First', False)
    channels_create_v1(first_id, 'Second', True)
    assert(channels_list_v1(first_id) != {})


# Testing if channels linked to specified users are listed
def test_2_multiple_users_multiple_channels():
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    second_id = auth_register_v1(
        'fakeas2@gmail.com', 'fakepassword2', 'Tom', 'Daniels')['auth_user_id']
    channels_create_v1(first_id, 'First', True)
    channels_create_v1(second_id, 'Second', False)
    assert(channels_list_v1(first_id) != {})
    assert(channels_list_v1(second_id) != {})


# Testing if channels linked to specified users are listed
def test_3_user_no_channel():
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    second_id = auth_register_v1(
        'fakeas2@gmail.com', 'fakepassword2', 'Tom', 'Daniels')['auth_user_id']
    channels_create_v1(first_id, "First", True)
    assert(channels_list_v1(second_id) == {'channels': []})


# Testing if invalid user raises an AccessError
def test_4_invalid_user():
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    first_channel = channels_create_v1(first_id, 'First', True)
    with pytest.raises(AccessError):
        channels_list_v1(first_id + 1)


# Test for channels_listall_v1

# Testing output type as the testing requires going into the data
def test_0_output_type():
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    first_channel = channels_create_v1(first_id, 'First', True)
    second_channel = channels_create_v1(first_id, 'Second', True)
    assert(channels_listall_v1(first_id) != {})


# Testing if invalid user raises an AccessError
def test_1_invalid_user():
    clear_v1()
    first_id = auth_register_v1(
        'fakeas@gmail.com', 'fakepassword', 'Calvin', 'Do')['auth_user_id']
    first_channel = channels_create_v1(first_id, "First", True)
    with pytest.raises(AccessError):
        channels_listall_v1(first_id + 1)


# channels_create_v1 tests
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
