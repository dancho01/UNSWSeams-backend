import pytest
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1, channel_details_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
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

# creates first user and PUBLIC channel
@pytest.fixture
def create_first_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'first_new_channel_id': first_new_channel_id}

# creates first user and PRIVATE channel
@pytest.fixture
def create_first_private_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_private_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', False)['channel_id']
    return {'auth_user1_id': auth_user1_id, 
        'first_new_private_channel_id': first_new_private_channel_id}

@pytest.fixture
def create_second_user():
    auth_user2_id = auth_register_v1('another_email@domain.com',
                                     'Password2', 'First', 'Last')['auth_user_id']
    return {'auth_user2_id': auth_user2_id}

@pytest.fixture
def create_third_user():
    auth_user3_id = auth_register_v1('third_email@domain.com',
                                     'Password3', 'First', 'Last')['auth_user_id']
    return {'auth_user3_id': auth_user3_id}

'''
Tests for channel_invite_v1
'''
'''
    Testing single errors for channel_invite_v1
'''

def test_invite_invalid_channel_id(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        1
    Error raised: 
        InputError 
    Explanation: 
        When the given channel does not exist, throw an input error. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(InputError): 
        channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'] + 1, auth_user2_id)


def test_invite_invalid_u_id(create_first_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        1
    Error raised: 
        InputError 
    Explanation: 
        When the user being invited does not exist, throw an input error. 
    '''
    info = create_first_channel_and_user
    with pytest.raises(InputError):
        channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'], info['auth_user1_id'] + 1)


def test_invite_already_channel_member(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        1
    Error raised: 
        InputError 
    Explanation: 
        When the user being invited is already a member of the channel, throw an input error. 
    '''
    # tests that u_id is already in the channel
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    print(auth_user2_id, info)
    channel_join_v1(auth_user2_id, info['first_new_channel_id'])
    with pytest.raises(InputError):  # should raise an exception
        channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'], auth_user2_id)



def test_invite_auth_user_not_in_channel(create_first_user, create_second_user, create_first_channel_and_user, create_third_user):
    '''
    No. of errors tested: 
        1
    Error raised: 
        AccessError 
    Explanation: 
        When the user who is calling the function is not a member of the channel they are inviting users to. 
        Throw an AccessError as users can only invite others to a channel if they are already a member of that
        channel.

        User 1 and User 2 are both not members of the channel, and the given channel exists, 
        so no input error should be raised. 
        Just testing an AccessError by itself. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    auth_user3_id = create_third_user['auth_user3_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user2_id, info['first_new_channel_id'], auth_user3_id)


def test_invite_invalid_auth_user_id(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        1
    Error raised: 
        AccessError 
    Explanation: 
        When the user calling the function does not exist, throw an AccessError. 
        All other inputs exist so not testing any input errors. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user2_id + 1, info['first_new_channel_id'], auth_user2_id)

'''
Testing multiple simultaneous errors for channel_invite_v1
'''

def test_invite_2_input_errors(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2 Input Errors
    Error raised: 
        InputError 
    Explanation: 
        Testing 2 input errors: invalid channel & invalid u_id
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(InputError):
        channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'] + 1, auth_user2_id + 1)

    '''
    Testing both input and access errors - AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''

def test_invite_invalid_auth_invalid_channel(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function does not exist.  
        InputError: When the channel is invalid, 
        
        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user2_id + 1, info['first_new_channel_id'] + 1, auth_user2_id)


def test_invite_invalid_auth_invalid_u_id(create_first_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function does not exist. 
        InputError: When the user being invited does not exist.

        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_invite_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'], info['auth_user1_id'] + 2)


    # test 1 access 1 input error

def test_invite_invalid_auth_id_inviting_existing_member(create_first_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function does not exist. 
        InputError: When the user being invited is already a channel member. 

        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    # test auth_user_id doesn't exist & u_id already a member
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_invite_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'], info['auth_user1_id'])


    # test 1 access 1 input error


def test_invite_unauthorised_auth_id_inviting_non_registered_user(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function is not a member of the given channel. 
        InputError: When the user being invited does not exist. 

        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user2_id, info['first_new_channel_id'], auth_user2_id + 1)

    # test 1 access 1 input error


def test_invite_unauthorised_auth_id_inviting_existing_channel_member(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        2
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function is not a member of the given channel. 
        InputError: When the user being invited is already a channel member. 

        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user2_id, info['first_new_channel_id'], info['auth_user1_id'])

def test_invite_invalid_auth_invalid_u_id_invalid_channel(create_first_user, create_first_channel_and_user):
    '''
    No. of errors tested: 
        3
    Error raised: 
        AccessError 
    Explanation: 
        AccessError: When the user calling the function does not exist. 
        InputError: When the user being invited does not exist. 
        InputError: When the given channel does not exist.

        AccessErrors should be called when both Input and Access Errors can be thrown. 
    '''
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_invite_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'] + 1, info['auth_user1_id'] + 2)

def test_invited_user_in_channel_after_invite(create_first_user, create_second_user, create_first_channel_and_user):
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'], auth_user2_id)

    assert(channels_list_v1(auth_user2_id) != {})


'''
Tests for channel_details_v1
'''


def test_details_invalid_auth_user_id(create_first_user, create_first_channel_and_user):
    '''
    Error raised:
        AccessError 
    Explanation: 
        When the user calling the function does not exist
    '''
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_details_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'])


def test_details_auth_user_not_in_channel(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    Error raised: 
        AccessError 
    Explanation: 
        When the user calling the function is not a member of the channel, and the channel id is valid. 
        Therefore the user does not have permission to see the channel's details. 
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_details_v1(auth_user2_id, info['first_new_channel_id'])


def test_details_invalid_channel(create_first_user, create_first_channel_and_user):
    '''
    Error raised: 
        InputError

    Explanation: 
        When the given channel does not exist, raise an input error. 
    '''
    info = create_first_channel_and_user
    with pytest.raises(InputError):
        channel_details_v1(info['auth_user1_id'], info['first_new_channel_id'] + 1)


def test_details_return_type(create_first_user, create_first_channel_and_user):
    '''
    Tests that the channel_details function returns a dictionary. 
    '''
    info = create_first_channel_and_user
    channel_details = channel_details_v1(info['auth_user1_id'], info['first_new_channel_id'])
    assert type(channel_details) == dict


# tests for channel_messages_v1

def test_invalid_channel_user_id():
    clear_v1()
    auth_register_v1('bob.smith@gmail.com', 'comp1531', 'Bob', 'Smith')
    first_auth_id = auth_login_v1(
        'bob.smith@gmail.com', 'comp1531').get('auth_user_id')
    valid_channel_id = channels_create_v1(
        first_auth_id, 'first_channel', True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(first_auth_id + 1, valid_channel_id, 0)

# length of the messages should be 0 as when a channel gets created, messages is a empty list.


def test_invalid_channel_start_index():
    clear_v1()
    auth_register_v1('bob.smith@gmail.com', 'comp1531', 'Bob', 'Smith')
    first_auth_id = auth_login_v1(
        'bob.smith@gmail.com', 'comp1531').get('auth_user_id')
    valid_channel_id = channels_create_v1(
        first_auth_id, 'first_channel', True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(first_auth_id, valid_channel_id, 3)


def test_invalid_channel_channel_id():
    clear_v1()
    auth_register_v1('bob.smith@gmail.com', 'comp1531', 'Bob', 'Smith')
    first_auth_id = auth_login_v1(
        'bob.smith@gmail.com', 'comp1531').get('auth_user_id')
    valid_channel_id = channels_create_v1(
        first_auth_id, 'first_channel', True)['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(first_auth_id, valid_channel_id + 1, 0)


def test_channel_no_messages():
    clear_v1()
    auth_register_v1('bob.smith@gmail.com', 'comp1531', 'Bob', 'Smith')
    first_auth_id = auth_login_v1(
        'bob.smith@gmail.com', 'comp1531').get('auth_user_id')
    valid_channel_id = channels_create_v1(
        first_auth_id, 'first_channel', True)['channel_id']
    assert(channel_messages_v1(first_auth_id,
           valid_channel_id, -1)['messages'] == [])


def test_channel_messages_user_no_auth():
    clear_v1()
    auth_register_v1('bob.smith@gmail.com', 'comp1531', 'Bob', 'Smith')
    auth_register_v1('john.appleseed@gmail.com',
                     'hello123', 'John', 'Appleseed')
    first_auth_id = auth_login_v1(
        'bob.smith@gmail.com', 'comp1531').get('auth_user_id')
    second_auth_id = (auth_login_v1(
        'john.appleseed@gmail.com', 'hello123').get('auth_user_id'))
    valid_channel_id = channels_create_v1(
        first_auth_id, 'first_channel', True)['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(second_auth_id, valid_channel_id, 0)


'''
channel_join_v1 tests
'''

def test_invalid_channel_id(create_first_user, create_second_user, create_first_channel_and_user):
    '''
    InputError as user is trying to join a channel that does not yet exist
    '''
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(InputError):
        channel_join_v1(info['auth_user1_id'], info['first_new_channel_id'] + 1)


def test_auth_user_already_member(create_first_user, create_first_channel_and_user):
    """
    InputError as user is already a member of the channel
    """
    info = create_first_channel_and_user
    with pytest.raises(InputError):
        channel_join_v1(info['auth_user1_id'], info['first_new_channel_id'])


def test_join_priv_channel(create_first_user, create_first_private_channel_and_user, create_second_user):
    """
    AccessError is thrown as user 2, who is not channel member/global owner, tries to join private channel
    """
    # user 1 (global owner) creates a private channel, making him channel owner/member
    info = create_first_private_channel_and_user
    # user 2 is registered (not a global owner)
    auth_user2_id = create_second_user['auth_user2_id']
    with pytest.raises(AccessError):
        channel_join_v1(auth_user2_id, info['first_new_private_channel_id'])


def test_invalid_auth_user_id(create_first_user, create_first_channel_and_user):
    """
    AccessError is thrown as auth_user_id does not exist
    """
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_join_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'])


def test_invalid_channel_id_and_user_id(create_first_user, create_first_channel_and_user):
    """
    Testing multiple errors: 
    1. InputError: invalid channel id
    2. AccessError: invalid user id 
    Access Error is called where both Access and Input errors can be raised
    """
    info = create_first_channel_and_user
    with pytest.raises(AccessError):
        channel_join_v1(info['auth_user1_id'] + 1, info['first_new_channel_id'] + 1)


def test_correct_return_type(create_first_user, create_second_user, create_first_channel_and_user):
    """
    Test that the function returns an empty dictionary
    """
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    # success case
    assert channel_join_v1(auth_user2_id, info['first_new_channel_id']) == {}

def test_user_added(create_first_user, create_second_user, create_first_channel_and_user):
    """
    Test that user is successfully added to channel, by testing that they cannot be invited again
    """
    info = create_first_channel_and_user
    auth_user2_id = create_second_user['auth_user2_id']
    channel_join_v1(auth_user2_id, info['first_new_channel_id'])
    # should not be able to invite user 2 to this channel again
    with pytest.raises(InputError):
        channel_invite_v1(info['auth_user1_id'], info['first_new_channel_id'], auth_user2_id)
