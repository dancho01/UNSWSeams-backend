import pytest
import requests
import random
import string
import json
from src import config
from datetime import datetime, timezone

@pytest.fixture
def create_future_time():
    # datetime(year, month, day, hour, minute, second, microsecond)
    future_time = datetime(2022, 11, 28, 23, 55, 59, 342380)
    return future_time

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


def test_message_sendlater_invalid_channel_id(create_public_channel, generate_invalid_message, create_future_time):
    '''
    Input Error when channel_id does not refer to a valid channel
    '''
    user1_data = create_public_channel[1]
    channel1 = create_public_channel[0]
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'] + 1, 'message': 'hello', 'time_sent': create_future_time})

    assert response.status_code == 400  # InputError


def test_message_sendlater_message_too_long(create_public_channel, generate_invalid_message, create_future_time):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is 1500 character string that is randomly generated
    '''
    new_message = generate_invalid_message
    response = requests.put(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': new_message, 'time_sent': create_future_time})

    assert response.status_code == 400  # InputError

def test_message_sendlater_empty_message(create_public_channel, generate_invalid_message, create_future_time):
    '''
    Error Raised:
        Input Error: length of message is less than 1 or over 1000 characters
    Explanation:
        New_message is empty
    '''
    new_message = ''
    response = requests.put(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': new_message, 'time_sent': create_future_time})

    assert response.status_code == 400  # InputError

def test_message_sendlater_invalid_time():
    '''
    Error Raised:
        Input Error: time_sent is a time in the past
    Explanation:
        time_set is in 2018
    '''
    past_time = datetime(2018, 11, 28, 23, 55, 59, 342380)
    response = requests.put(config.url + 'message/sendlater/v1', json={'token': user1_data['token'], 
                    'channel_id': channel1['channel_id'], 'message': new_message, 'time_sent': past_time})

    assert response.status_code == 400  # InputError

def test_message_sendlater_not_member(create_second_user, create_future_time):
    '''
    Error Raised:
        AccessError: channel_id is valid and the authorised user is not a member of the channel they are trying to post to
    '''
    user2_data = create_second_user
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user2_data['token'], 'channel_id': channel1['channel_id'], 'message': 'hello', 'time_sent': create_future_time})

    assert response.status_code == 403  # AccessError

def test_message_sendlater_success(create_future_time):
    '''
    Sucess case: user 1 successfully schedules a message to be sent later to a channel they are a member of
    '''
    response = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'], 'message': 'hello', 'time_sent': create_future_time})

    assert response.status_code == 200  # Success
    