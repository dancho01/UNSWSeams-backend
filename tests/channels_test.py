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
# Tests for invalid name for public channel
def test_invalid_channel_name_public(create_first_user): 
    '''
    '''  
    first_u_id = create_first_user['auth_user1_id']
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, '', True)
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, 'abcdefghijklmnopqrstuvwxyz', True)

# Tests for invalid name for private channel
def test_invalid_channel_name_private(create_first_user):
    '''
    
    '''
    first_u_id = create_first_user['auth_user1_id']
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, '', False)
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, 'abcdefghijklmnopqrstuvwxyz', False)

# Tests for invalid user_id and invalid channel name 
def test_invalid_name_and_user_id():
    '''
    
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, '', True)
    with pytest.raises(AccessError):
        channels_create_v1(1, 'abcdefghijklmnopqrstuvwxyz', True)

# Test for invalid user id passed in
def test_no_user_registered():
    '''
    
    
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1(1, 'channelname', True)

# Test for correct return type
def test_correct_return_type(create_first_channel_and_user):
    '''
    
    '''
    channel_return = create_first_channel_and_user
    channel_id = channel_return['first_new_channel_id']
    assert type(channel_id) is int
    
