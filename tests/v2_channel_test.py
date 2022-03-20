# HTTP tests for v2 channel.py
import pytest
import requests
import json
from src import config

@pytest.fixture
def create_first_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    return user1
    # is this fixture's return type correct?
"""
# creates first user and PUBLIC channel


@pytest.fixture
def create_first_channel_and_user(create_first_user):
    auth_user1_id = create_first_user['auth_user1_id']
    first_new_channel_id = channels_create_v1(
        auth_user1_id, 'Channel Name', True)['channel_id']
    return {'auth_user1_id': auth_user1_id,
            'first_new_channel_id': first_new_channel_id}
"""

def test_invite_invalid_channel(create_first_user):
    '''
    A simple test to check invalid channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})

    response = requests.post(config.url + 'channel/invite/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'] + 1, 
        'u_id': user2['token']})    # don't know how to name a non existent channel id
    assert response.status_code == 400  # inputError

def test_invite_invalid_u_id(create_first_user): 
    '''
    A simple test to check invalid u_id
    '''
    user1 = create_first_user()
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})

    response = requests.post(config.url + 'channel/invite/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'], 
        'u_id': 'nonexistent_token'})    # don't know how to name a non existent user id
    assert response.status_code == 400  # inputError

def test_invite_already_channel_member(create_first_user):
    '''
    A simple test to check already channel member
    '''
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    requests.post(config.url + 'channel/join/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id']})
    response = requests.post(config.url + 'channel/invite/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'], 
        'u_id': user2['token']})    # don't know how to name a non existent user id
    assert response.status_code == 400  # inputError

def test_invite_auth_user_not_in_channel(create_first_user):
    '''
    A simple test to check auth_user not in channel
    '''
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user3 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email3@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/invite/v2', params={'token': user3['token'], 'channel_id': channel_1['channel_id'], 
        'u_id': user2['token']})    
    assert response.status_code == 403  # AccessError

def test_invite_invalid_auth_user_id(create_first_user):
    '''
    A simple test to check valid token
    '''
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/invite/v2', params={'token': 'nonexistent_token', 'channel_id': channel_1['channel_id'], 
        'u_id': user2['token']})    # don't know how to name a non existent user id
    assert response.status_code == 403  # AccessError

"""
    Tests for channel/join/v2
"""

def test_invalid_channel_id(create_first_user):
    '''
    A simple test to check if channel_id is valid
    '''
    user1 = create_first_user()
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/join/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'] + 1})
    assert response.status_code == 400  # inputError

def test_auth_user_already_member(create_first_user):
    '''
    A simple test to check if user already a member of the channel
    '''
    user1 = create_first_user()
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/join/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id']})
    assert response.status_code == 400  # inputError

def test_join_priv_channel(create_first_user):
    '''
    A simple test to check that non-global owner can join a private channel they are not invited to
    '''
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': False})
    response = requests.post(config.url + 'channel/join/v2', params={'token': user2['token'], 'channel_id': channel_1['channel_id']})
    assert response.status_code == 400  # inputError

def test_invalid_auth_user_id(create_first_user):
    """
    403 status code (AccessError) is returned as token does not exist
    """
    user1 = create_first_user()
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/join/v2', params={'token': 'nonexistent_token', 'channel_id': channel_1['channel_id']})
    assert response.status_code == 403  # AccessError

def test_invalid_channel_id_and_user_id(create_first_user):
    """
    Testing multiple errors: 
    1. InputError: invalid channel id
    2. AccessError: invalid user id 
    Access Error is called where both Access and Input errors can be raised
    """
    user1 = create_first_user()
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/join/v2', params={'token': 'nonexistent_token', 'channel_id': channel_1['channel_id'] + 1})
    assert response.status_code == 403  # AccessError

def test_correct_return_type(create_first_user):
    """
    Test that the function returns an empty dictionary
    """
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response = requests.post(config.url + 'channel/join/v2', params={'token': user2['token'], 'channel_id': channel_1['channel_id']})
    assert json.loads(response.text ) == {} 
    # not sure if this is how it works?

def test_user_added(create_first_user):
    """
    Test that user is successfully added to channel, by testing that they cannot be invited again
    """
    user1 = create_first_user()
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})
    response1 = requests.post(config.url + 'channel/join/v2', params={'token': user2['token'], 'channel_id': channel_1['channel_id']})
    assert response1.status_code == 200
    response2 = requests.post(config.url + 'channel/invite/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'], 
        'u_id': user2['token']})
    assert response2.status_code == 400 # InputError