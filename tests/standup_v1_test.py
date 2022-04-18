import pytest
import requests
import random
import string
import time
from src import config

''' fixtures '''


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


@pytest.fixture
def generate_invalid_message():
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(1010))
    return invalid_message


''' tests for standup/start/v1 '''


def test_standup_start_invalid_channel(create_first_user):
    '''
    Tests when channel_id passed in is invalid , resulting in InputError
    
    '''

    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    response = requests.post(config.url + 'standup/start/v1', json={
                             'token': user['token'], 'channel_id': channel_id['channel_id'] + 1, 'length': 2})

    assert response.status_code == 400


def test_standup_start_negative_length(create_first_user):
    '''
    Tests when length passed in is a negative integer, resulting in InputError
    
    '''

    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})

    channel_id = channel_id_resp.json()

    response = requests.post(config.url + 'standup/start/v1',
                             json={'token': user['token'], 'channel_id': channel_id['channel_id'], 'length': -10})

    assert response.status_code == 400


def test_standup_start_already_running(create_first_user):
    '''
    Tests attempting to start a standup when there is already one running in the channel,
    resulting in InputError
    '''
    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                                    'channel_id': channel_id['channel_id'], 'length': 1})

    assert response.status_code == 400


def test_standup_start_unauthorised_user(create_first_user, create_second_user):
    '''
    Tests when authorised user is not a member of the channel that user is 
    trying to start standup in, resulting in AccessError
    
    '''
    user1 = create_first_user
    user2 = create_second_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    response = requests.post(config.url + 'standup/start/v1', json={'token': user2['token'],
                                                                    'channel_id': channel_id['channel_id'], 'length': 1})

    assert response.status_code == 403


def test_standup_start_success(create_first_user):
    '''
    Tests when standup is successfully started by user
    '''
    user = create_first_user
    
    requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})    
    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'Second Channel', 'is_public': True})
    channel_id = channel_id_resp.json()
    
    requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'Third Channel', 'is_public': True}) 

    response = requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                                    'channel_id': channel_id['channel_id'], 'length': 1})
    time.sleep(3)

    assert response.status_code == 200


''' tests for standup/active/v1 '''


def test_standup_active_invalid_channel(create_first_user):
    '''
    Tests when channel_id passed in is invalid, resulting in InputError
    '''

    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.get(config.url + 'standup/active/v1', params={'token': user['token'],
                                                                      'channel_id': channel_id['channel_id'] + 1})

    assert response.status_code == 400


def test_standup_active_unauthorised_user(create_first_user, create_second_user):
    '''
    Tests when channel_id is valid and the authorised user is not a member of 
    the channel, resulting in AccessError
    
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user1['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.get(config.url + 'standup/active/v1', params={'token': user2['token'],
                                                                      'channel_id': channel_id['channel_id']})

    assert response.status_code == 403


def test_standup_active_success(create_first_user):
    '''
    Tests successful return in the case that standup is active in channel
    
    '''
    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 5})

    response = requests.get(config.url + 'standup/active/v1', params={'token': user['token'],
                                                                      'channel_id': channel_id['channel_id']})
    assert response.status_code == 200
    
def test_standup_not_active_success(create_first_user):
    '''
    Tests successful return in the case that standup is NOT active in channel
    '''
    user = create_first_user

    requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'Second Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    response = requests.get(config.url + 'standup/active/v1', params={'token': user['token'],
                                                                      'channel_id': channel_id['channel_id']})
    assert response.status_code == 200


''' tests for standup/send/v1 '''

def test_standup_send_invalid_channel(create_first_user):
    '''
    Tests when channel_id passed in is invalid, resulting in InputError
    '''

    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.post(config.url + 'standup/send/v1', json={'token': user['token'],
                                                                   'channel_id': channel_id['channel_id'] + 1, 'message': 'This is message'})

    assert response.status_code == 400


def test_standup_send_invalid_length_message(create_first_user, generate_invalid_message):
    '''
    Tests when length of message is over 1000 characters, resulting in InputError
    
    '''

    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.post(config.url + 'standup/send/v1', json={'token': user['token'],
                                                                   'channel_id': channel_id['channel_id'], 'message': generate_invalid_message})

    assert response.status_code == 400


def test_standup_send_not_currently_active(create_first_user):
    '''
    Tests sending a message to a standup not currently running, resulting in InputError
    '''
    user = create_first_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    response = requests.post(config.url + 'standup/send/v1', json={'token': user['token'],
                                                                   'channel_id': channel_id['channel_id'], 'message': 'this is a message'})

    assert response.status_code == 400


def test_standup_send_unauthorised_user(create_first_user, create_second_user):
    '''
    Tests when channel_id is valid and the authorised user is not a member of 
    the channel, resulting in AccessError
    
    '''
    user1 = create_first_user
    user2 = create_second_user

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                             'name': 'First Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user1['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.post(config.url + 'standup/send/v1', json={'token': user2['token'],
                                                                   'channel_id': channel_id['channel_id'], 'message': 'this is a message'})

    assert response.status_code == 403


def test_standup_send_success(create_first_user):
    '''
    Tests when standup/send/v1 is successful
    '''
    user1 = create_first_user

    requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                             'name': 'First Channel', 'is_public': True})

    channel_id_resp = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                             'name': 'Second Channel', 'is_public': True})
    channel_id = channel_id_resp.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user1['token'],
                                                         'channel_id': channel_id['channel_id'], 'length': 1})

    response = requests.post(config.url + 'standup/send/v1', json={'token': user1['token'],
                                                                   'channel_id': channel_id['channel_id'], 'message': 'this is a message'})

    assert response.status_code == 200
