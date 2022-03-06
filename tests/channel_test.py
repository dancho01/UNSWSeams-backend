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


'''
Tests for channel_invite_v1
'''


def test_invite_invalid_channel_id(create_first_user, create_second_user, create_first_channel_and_user):
    # auth_user_id = auth_register_v1(
    #     'valid_email@domain.com', 'Password1', 'First', 'Last')['auth_user_id']
    channel_user_return = create_first_channel_and_user
    auth_user2_id = create_second_user
    with pytest.raises(InputError):  # should raise an exception
        channel_invite_v1(channel_user_return['auth_user1_id'],
                          channel_user_return['first_new_channel_id'] + 1, auth_user2_id)


def test_invite_invalid_u_id():
    clear_v1()
    auth_user_id = auth_register_v1(
        'valid_email@domain.com', 'Password1', 'First', 'Last')['auth_user_id']
    new_channel = channels_create_v1(
        auth_user_id, 'Channel Name', True)['channel_id']

    with pytest.raises(InputError):
        # assume u_id 3 does not exist
        channel_invite_v1(auth_user_id, new_channel, auth_user_id + 1)


def test_invite_already_channel_member():
    # tests that u_id is already in the channel

    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name', True)[
        'channel_id']   # returns an integer channel_id
    channel_join_v1(u_id2, channel1)

    with pytest.raises(InputError):
        channel_invite_v1(u_id1, channel1, u_id2)


def test_invite_auth_user_not_in_channel():
    # test both users not in channel and channel_id is valid
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    u_id3 = auth_register_v1('third_email@domain.com',
                             'Password3', 'First', 'Last')['auth_user_id']

    channel1 = channels_create_v1(u_id3, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id
    with pytest.raises(AccessError):
        channel_invite_v1(u_id1, channel1, u_id2)


def test_invite_invalid_auth_user_id():
    # when auth_user_id does not exist
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name', True)[
        'channel_id']   # returns an integer channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id2 + 1, channel1, u_id2)

    # test multiple errors


def test_invite_all_input_errors():
    # all three input errors
    # so auth user not in channel, and channel is invalid, u_id invalid
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']

    channel1 = channels_create_v1(u_id2, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    with pytest.raises(InputError):
        channel_invite_v1(u_id1, channel1 + 1, u_id2 + 1)

    # test both input and access errors - access errors should be called first

    # test 1 access 1 input error


def test_invite_invalid_auth_invalid_channel():
    # test auth_user_id doesn't exist & invalid channel
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id2 + 1, channel1 + 1, u_id2)

    # test 1 access 1 input error


def test_invite_invalid_auth_invalid_u_id():
    # test auth_user_id doesn't exist & u_id doesn't exist
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id1 + 1, channel1, u_id1 + 2)

    # test 1 access 1 input error


def test_invite_invalid_auth_id_inviting_existing_member():
    # test auth_user_id doesn't exist & u_id already a member
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id1 + 1, channel1, u_id1)

    # test 1 access 1 input error


def test_invite_unauthorised_auth_id_inviting_non_registered_user():
    # test auth_user_id not a member of channel & invalid u_id
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id2, channel1, u_id2 + 1)

    # test 1 access 1 input error


def test_invite_unauthorised_auth_id_inviting_existing_channel_member():
    # test auth_user_id not a member of channel & invalid u_id
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']
    channel1 = channels_create_v1(u_id1, 'Channel Name',
                                  True).get('channel_id')  # returns channel_id

    with pytest.raises(AccessError):
        channel_invite_v1(u_id2, channel1, u_id1)


def test_invited_user_in_channel_after_invite():
    clear_v1()
    u_id1 = auth_register_v1('valid_email@domain.com',
                             'Password1', 'First', 'Last')['auth_user_id']
    u_id2 = auth_register_v1('another_email@domain.com',
                             'Password2', 'First', 'Last')['auth_user_id']

    channel1 = channels_create_v1(u_id2, 'Channel Name',
                                  True).get('channel_id')   # returns channel_id

    channel_invite_v1(u_id2, channel1, u_id1)

    assert(channels_list_v1(u_id1) != {})


'''
Tests for channel_details_v1
'''


def test_details_invalid_auth_user_id(create_first_channel_and_user):
    '''
    Error raised:
        AccessError: Checking if auth_user_id passed in is invalid.

    Explanation:
        Pytest fixture create_first_channel_and_user is run, the 'auth_user1_id' + 1 is 
        passed in as an argument for channel_details_v1. Since this id does not exist
        then AccessError is raised.
    '''
    with pytest.raises(AccessError):
        channel_details_v1(
            create_first_channel_and_user['auth_user1_id'] + 1,
            create_first_channel_and_user['first_new_channel_id'])


def test_details_auth_user_not_in_channel(create_first_channel_and_user, create_second_user):
    '''
    Error raised:
        AccessError: Checking if auth_user_id passed in is invalid.

    Explanation:
        Pytest fixture create_first_channel_and_user is run, the 'auth_user1_id' + 1 is 
        passed in as an argument for channel_details_v1. Since this id does not exist
        then AccessError is raised.
    '''
    with pytest.raises(AccessError):
        channel_details_v1(
            create_second_user, create_first_channel_and_user['first_new_channel_id'])


def test_details_invalid_channel(create_first_channel_and_user):
    '''
    Error raised:
        InputError: Occurs when channel_id does not refer to a valid channel

    Explanation:
        Channel details will raise an input error if the channel_id is invalid. Here we only
        register one channel from the create_first_channel_and_user fixture, we input the 
        channel_id returned from the fixture and pass that channel_id + 1 as an argument which
        is not a valid channel.
    '''
    with pytest.raises(InputError):
        channel_details_v1(
            create_first_channel_and_user['auth_user1_id'], create_first_channel_and_user['first_new_channel_id'] + 1)


def test_details_return_type(create_first_channel_and_user):
    '''
    Return checked:
        Checking to see if details returns a dictionary structure

    Explanation:
        This test creates a user and a channel, it then checks if when channel_details_v1
        is called with valid arguments, if it will return the correct datastructure.
    '''
    assert type(channel_details_v1(
        create_first_channel_and_user['auth_user1_id'], create_first_channel_and_user['first_new_channel_id'])) == dict


'''
tests for channel_messages_v1
'''


def test_invalid_channel_user_id(create_first_channel_and_user):
    '''
    Error raised:
        AccessError: Occurs when auth_user_id passed in is invalid

    Explanation:
        Passes in a valid auth_user_id + 1 which is not registered, expected outcome should 
        be an access error.
    '''

    with pytest.raises(AccessError):
        channel_messages_v1(
            create_first_channel_and_user['auth_user1_id'] + 1, create_first_channel_and_user['first_new_channel_id'], 0)


def test_invalid_channel_start_index(create_first_channel_and_user):
    '''
    Error raised:
        InputError: Occurs when start is greater than the total number of messages in the channel

    Explanation:
        Both auth_user_id and channel_id is valid, all channels have 0 messages, so if start is >= 0,
        an InputError is raised.
    '''
    with pytest.raises(InputError):
        channel_messages_v1(
            create_first_channel_and_user['auth_user1_id'],
            create_first_channel_and_user['first_new_channel_id'], 3)


def test_invalid_channel_channel_id(create_first_channel_and_user):
    '''
    Error raised:
        InputError: Occurs when channel_id does not refer to a valid channel

    Explanation:
        Valid auth_user_id and channel_id from create_first_channel_and_user fixture,
        however the 1 is added to the valid channel_id when being passed into
        channel_messages_v1 making it invalid. Should raise InputError.
    '''
    with pytest.raises(InputError):
        channel_messages_v1(create_first_channel_and_user['auth_user1_id'],
                            create_first_channel_and_user['first_new_channel_id'] + 1, 0)


def test_channel_messages_user_no_auth(create_first_channel_and_user, create_second_user):
    '''
    Error raised:
        AccessError: Occurs when channel_id is valid and the authorized user is not a member of the channel

    Explanation:
        The first channel is registered under the first users id, the second user then requests
        the channel messages but an error is raised as he is not apart of the 'all_users' of 
        that channel.
    '''
    with pytest.raises(AccessError):
        channel_messages_v1(
            create_second_user['auth_user2_id'], create_first_channel_and_user['first_new_channel_id'], 0)


'''
channel_join_v1
'''


def test_0_invalid_channel_id():
    clear_v1()
    auth_register_return = auth_register_v1(
        'randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_register_return.get('auth_user_id')
    # InputError as user is trying to join a channel that does not yet exist
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id, 1)


def test_1_auth_user_already_member():
    clear_v1()
    auth_register_return = auth_register_v1(
        'randomuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id = auth_register_return.get('auth_user_id')
    channels_result = channels_create_v1(auth_user_id, 'validname', True)
    channel_id = channels_result.get('channel_id')
    # InputError is thrown as authorised user is already a channel member
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id, channel_id)


def test_2_join_priv_channel():
    clear_v1()
    auth_register_return = auth_register_v1(
        'firstuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id_1 = auth_register_return.get('auth_user_id')
    # user 1 (global owner) creates a private channel, making him channel owner/member
    channels_result = channels_create_v1(auth_user_id_1, 'validname', False)
    channel_id = channels_result.get('channel_id')
    # user 2 is registered (not a global owner)
    auth_register_return = auth_register_v1(
        'seconduser@gmail.com', 'password', 'firstname', 'lastname')
    auth_user_id_2 = auth_register_return.get('auth_user_id')
    with pytest.raises(AccessError):
        channel_join_v1(auth_user_id_2, channel_id)
    # AccessError is thrown as user 2, who is not channel member/global owner, tries to join private channel


def test_3_invalid_auth_user_id():
    clear_v1()
    auth_register_return = auth_register_v1(
        'firstuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id_1 = auth_register_return.get('auth_user_id')
    channels_result = channels_create_v1(auth_user_id_1, 'validname', True)
    channel_id = channels_result.get('channel_id')
    with pytest.raises(AccessError):
        channel_join_v1(auth_user_id_1 + 1, channel_id)


def test_invalid_channel_id_and_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channel_join_v1(1, 1)


def test_4_correct_return_type():
    clear_v1()
    auth_register_return = auth_register_v1(
        'firstuser@gmail.com', 'password', 'Daniel', 'Cho')
    auth_user_id_1 = auth_register_return.get('auth_user_id')
    channels_result = channels_create_v1(auth_user_id_1, 'validname', True)
    channel_id = channels_result.get('channel_id')
    auth_register_return = auth_register_v1(
        'seconduser@gmail.com', 'password', 'firstname', 'lastname')
    auth_user_id_2 = auth_register_return.get('auth_user_id')
    # success case
    assert channel_join_v1(auth_user_id_2, channel_id) == {}
