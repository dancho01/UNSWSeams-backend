import pytest
import requests
import random
import string
import json
from src import config
from datetime import datetime, timezone
from src.channel_helper import time_now

@pytest.fixture
def create_future_timestamp():
    # datetime(year, month, day, hour, minute, second, microsecond)
    future_timestamp = time_now() + 3
    return future_timestamp

@pytest.fixture
def create_first_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    return user1_data


@pytest.fixture
def create_second_user():
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                             'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2_data = user2.json()
    return user2_data


@pytest.fixture
def create_public_channel():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    c1 = requests.post(config.url + 'channels/create/v2',
                       json={'token': user1_data['token'], 'name': 'ch1', 'is_public': True})
    channel1 = c1.json()

    return channel1, user1_data


@pytest.fixture
def generate_invalid_message():
    '''
    Generates a message over 1000 characters long
    '''
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(1500))
    return invalid_message


@pytest.fixture
def send_first_message():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    c1 = requests.post(config.url + 'channels/create/v2',
                       json={'token': user1_data['token'], 'name': 'ch1', 'is_public': True})
    channel1 = c1.json()
    response = requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'], 'message': "hello"})
    message_response = response.json()
    return message_response, user1_data, channel1

'''
    message/sendlater/v1 tests

'''


def test_message_sendlater_invalid_channel_id(create_future_timestamp):
    '''
    Input Error when channel_id does not refer to a valid channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    first_channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel1 = first_channel.json()
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'] + 1, 'message': 'hello', 'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError


def test_message_sendlater_message_too_long(generate_invalid_message, create_future_timestamp):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is 1500 character string that is randomly generated
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    first_channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel1 = first_channel.json()
    new_message = generate_invalid_message
    response = requests.post(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': new_message, 'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError

def test_message_sendlater_empty_message(create_public_channel, generate_invalid_message, create_future_timestamp):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is empty
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    first_channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel1 = first_channel.json()
    new_message = ''
    response = requests.post(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': new_message, 'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError

def test_message_sendlater_invalid_time():
    '''
    Error Raised:
        Input Error: time_sent is a time in the past
    Explanation:
        time_set is in 2018
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    first_channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel1 = first_channel.json()
    past_timestamp = time_now() - 2
    response = requests.post(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': 'hello', 'time_sent': past_timestamp})

    assert response.status_code == 400  # InputError

def test_message_sendlater_not_member(create_second_user, create_future_timestamp):
    '''
    Error Raised:
        AccessError: channel_id is valid and the authorised user is not a member of the channel they are trying to post to
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    first_channel = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel1 = first_channel.json()
    user2_data = create_second_user
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user2_data['token'], 'channel_id': channel1['channel_id'], 'message': 'hello', 'time_sent': create_future_timestamp})

    assert response.status_code == 403  # AccessError

def test_message_sendlater_success(create_future_timestamp, create_public_channel):
    '''
    Sucess case: user 1 successfully schedules a message to be sent later to a channel they are a member of
    '''
    
    user1_data = create_public_channel[1]
    channel1 = create_public_channel[0]
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'], 'message': 'hello', 'time_sent': create_future_timestamp})

    assert response.status_code == 200  # Success


# check that it actually runs 3 seconds later and not straight away or never

'''
    message/sendlaterdm/v1 tests

'''

def test_message_sendlaterdm_invalid_dm_id(create_future_timestamp, create_second_user):
    '''
    Input Error when channel_id does not refer to a valid channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })

    dm_response = requests.post(config.url + 'dm/create/v1', json = {
        'token': user1_data['token'] , 
        'u_ids': [2]})   
    assert dm_response.status_code == 200

    dm1 = dm_response.json()
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user1_data['token'], 
        'dm_id': dm1['dm_id'] + 1, 
        'message': 'hello', 
        'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError


def test_message_sendlaterdm_message_too_long(generate_invalid_message, create_future_timestamp, create_second_user):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is 1500 character string that is randomly generated
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [2]})
    dm1 = dm_response.json()
    new_message = generate_invalid_message
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user1_data['token'], 'dm_id': dm1['dm_id'], 'message': new_message, 'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError

def test_message_sendlaterdm_empty_message(create_public_channel, generate_invalid_message, create_future_timestamp, create_second_user):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is empty
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [2]})
    dm1 = dm_response.json()
    new_message = ''
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user1_data['token'], 'dm_id': dm1['dm_id'], 'message': new_message, 'time_sent': create_future_timestamp})

    assert response.status_code == 400  # InputError

def test_message_sendlaterdm_invalid_time(create_second_user):
    '''
    Error Raised:
        Input Error: time_sent is a time in the past
    Explanation:
        time_set is in 2018
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [2]})
    dm1 = dm_response.json()
    past_timestamp = time_now() - 2
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user1_data['token'], 'dm_id': dm1['dm_id'], 'message': 'hello', 'time_sent': past_timestamp})

    assert response.status_code == 400  # InputError


def test_message_sendlaterdm_not_member(create_second_user, create_future_timestamp):
    '''
    Error Raised:
        AccessError: channel_id is valid and the authorised user is not a member of the channel they are trying to post to
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user3_data = user3.json()
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [1]})
    dm1 = dm_response.json()
    
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user3_data['token'], 'dm_id': dm1['dm_id'], 'message': 'hello', 'time_sent': create_future_timestamp})

    assert response.status_code == 403  # AccessError

def test_message_sendlaterdm_success(create_future_timestamp, create_public_channel, create_second_user):
    '''
    Sucess case: user 1 successfully schedules a message to be sent later to a channel they are a member of
    '''
    
    user1_data = create_public_channel[1]
    user2_data = create_second_user
    user3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email3@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [2]})
    dm1 = dm_response.json()
    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user1_data['token'], 'dm_id': dm1['dm_id'], 'message': 'hello', 'time_sent': create_future_timestamp})


    assert response.status_code == 200  # Success
