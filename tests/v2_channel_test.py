# HTTP tests for v2 channel.py
import pytest
import requests
import json
from src import config


@pytest.fixture
def create_first_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    return user1_data


@pytest.fixture
def create_second_user():
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                                                 'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2_data = user2.json()
    return user2_data


# @pytest.fixture
# def create_first_channel_and_user(create_first_user):
#     auth_user1_id = create_first_user['auth_user1_id']
#     first_new_channel_id = channels_create_v1(
#         auth_user1_id, 'Channel Name', True)['channel_id']
#     return {'auth_user1_id': auth_user1_id,
#             'first_new_channel_id': first_new_channel_id}
# """

def test_invite_invalid_channel(create_first_user):
    '''
    A simple test to check invalid channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    invite_response = requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1,
                                                                            'u_id': user2_data['auth_user_id']})
    assert invite_response.status_code == 400  # inputError


def test_invite_invalid_u_id(create_first_user):
    '''
    A simple test to check invalid u_id
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    response = requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user1_data['auth_user_id'] + 1})
    assert response.status_code == 400  # inputError

def test_invite_already_channel_member(create_first_user):
    '''
    A simple test to check already channel member
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    response = requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # inputError


def test_invite_auth_user_not_in_channel(create_first_user):
    '''
    A simple test to check auth_user not in channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'email3@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user3_data = user3.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/invite/v2', json={'token': user3_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})
    assert response.status_code == 403  # AccessError

def test_invite_invalid_auth_user_id(create_first_user):
    '''
    A simple test to check valid token
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/invite/v2', json={'token': 'random_token', 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})
    assert response.status_code == 403  # AccessError

def test_invite_return_type():
    """
    check return type is empty dictionary
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})
    assert json.loads(response.text) == {}

"""
Tests for channel/join/v2
"""


def test_invalid_channel_id(create_first_user):
    '''
    A simple test to check if channel_id is valid
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1})
    assert response.status_code == 400  # inputError


def test_auth_user_already_member(create_first_user):
    '''
    A simple test to check if user already a member of the channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': user1_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert response.status_code == 400  # inputError


def test_join_priv_channel(create_first_user):
    '''
    A simple test to check that non-global owner cannot join a private channel they are not invited to
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': False})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert response.status_code == 403  # AccessError


def test_invalid_auth_user_id(create_first_user):
    """
    403 status code (AccessError) is returned as token does not exist
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': 'nonexistent_token', 'channel_id': channel_1_data['channel_id']})
    assert response.status_code == 403  # AccessError


def test_invalid_channel_id_and_user_id(create_first_user):
    """
    Testing multiple errors: 
    1. InputError: invalid channel id
    2. AccessError: invalid user id 
    Access Error is called where both Access and Input errors can be raised
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': 'nonexistent_token', 'channel_id': channel_1_data['channel_id'] + 1})
    assert response.status_code == 403  # AccessError

def test_correct_return_type(create_first_user):
    """
    Test that the function returns an empty dictionary
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user2_data['token'], 'name': 'First Channel',
        'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/join/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert json.loads(response.text) == {}

def test_user_added(create_first_user):
    """
    Test that user is successfully added to channel, by testing that they cannot be invited again
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})
    channel_1_data = channel_1.json()
    response1 = requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert response1.status_code == 200
    response2 = requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user2_data['token']})
    assert response2.status_code == 400 # InputError


"""
    channel/addowner/v1 tests
    Make user with user id u_id an owner of the channel.

    Arguments: 
    { token, channel_id, u_id }

    Returns: 
    {}
"""


def test_channel_addowner_invalid_channel(create_first_user):
    """
    channel_id does not refer to a valid channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1,
                                                                       'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # inputError


def test_channel_addowner_u_id_invalid(create_first_user):
    """
        u_id does not refer to a valid user
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                       'u_id': user1_data['auth_user_id'] + 1})
    assert response.status_code == 400  # inputError


def test_channel_addowner_user_not_member(create_first_user):
    """
        token refers to a user who is not a member of the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                       'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # InputError


def test_channel_addowner_user_already_owner():
    """
        u_id refers to a user who is already an owner of the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2',
                  json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                            'u_id': user2_data['auth_user_id']})
    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                       'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # inputError

def test_channel_addowner_user_no_owner_permission(create_first_user):
    """
        channel_id is valid and the authorised user does not have owner permissions in the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email3@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user3_data = user3.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user3_data['auth_user_id']})
    assert response.status_code == 403  # AccessError

def test_channel_addowner_return_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user2_data['auth_user_id']})
    assert response.status_code == 200  
    assert json.loads(response.text) == {}

"""
    Test channel/removeowner/v1

"""


def test_channel_removeowner_invalid_channel(create_first_user):
    """
    channel_id does not refer to a valid channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2',
                  json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                            'u_id': user2_data['auth_user_id']})

    response = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1,
                                                                       'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # inputError


def test_channel_removeowner_u_id_invalid(create_first_user):
    """
        u_id does not refer to a valid user
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                            'u_id': user2_data['auth_user_id']})
    response = requests.post(config.url + 'channel/removeowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                          'u_id': user2_data['auth_user_id'] + 1})
    assert response.status_code == 400  # inputError


def test_channel_removeowner_u_id_not_owner(create_first_user):
    """
        u_id refers to a user who is not an owner of the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2',
                  json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})

    response = requests.post(config.url + 'channel/removeowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                          'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # InputError


def test_channel_removeowner_user_only_owner(create_first_user):
    """
        u_id refers to a user who is currently the only owner of the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})        # created a private channel so only invitational.
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/invite/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user1_data['auth_user_id']})
    response = requests.post(config.url + 'channel/removeowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                          'u_id': user2_data['auth_user_id']})
    assert response.status_code == 400  # InputError

def test_channel_removeowner_user_no_owner_permissions():
    """
        channel_id is valid and the authorised user does not have owner permissions in the channel
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email3@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user3_data = user3.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    requests.post(config.url + 'channel/join/v2', json={'token': user3_data['token'], 'channel_id': channel_1_data['channel_id']})
    requests.post(config.url + 'channel/addowner/v1', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user3_data['auth_user_id']})
    response = requests.post(config.url + 'channel/removeowner/v1', json={'token': user3_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                          'u_id': user2_data['auth_user_id']})
    assert response.status_code == 403  # AccessError

def test_channel_removeowner_return_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email2@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email' : 'email3@gmail.com',
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user3_data = user3.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token': user1_data['token'], 'name': 'First Channel',
        'is_public': True})
    channel_1_data = channel_1.json()
    response1 = requests.post(config.url + 'channel/join/v2', json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert response1.status_code == 200  
    response2 = requests.post(config.url + 'channel/join/v2', json={'token': user3_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert response2.status_code == 200
    response3 = requests.post(config.url + 'channel/addowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
        'u_id': user3_data['auth_user_id']})
    assert response3.status_code == 200
    response4 = requests.post(config.url + 'channel/removeowner/v1', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                          'u_id': user3_data['auth_user_id']})
    assert response4.status_code == 200
    assert json.loads(response4.text) == {}