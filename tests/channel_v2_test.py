import pytest
import requests
import random
import string
import json
from src import config


@pytest.fixtures
def create_first_user():
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    return user1_data


@pytest.fixtures
def create_second_user():
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                                                 'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2_data = user2.json()
    return user2_data


@pytest.fixtures
def create_public_channel(create_first_user):
    c1 = requests.post(config.url + 'channels/create/v2',
                       json={'token': create_first_user['token'], 'name': 'ch1', 'is_public': True})
    return c1


@pytest.fixtures
def generate_invalid_message():
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(1500))
    return invalid_message


@pytest.Fixture
def send_first_message(create_first_user, create_public_channel):
    requests.delete(config.url + 'clear/v1')
    message = "hello"
    message_response = requests.get(config.url + 'message/send/v1', params={
        'token': create_first_user['token'], 'channel_id': create_public_channel['channel_id'], 'message': message})

    return message_response

# messages v2


def test_messages_invalid_channel(create_first_user, create_public_channel):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel    
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    requests.delete(config.url + 'clear/v1')
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': create_first_user['token'], 'channel_id': create_public_channel['channel_id'] + 1, 'start': 0})

    assert message_response.status_code == 400


def test_invalid_start(create_first_user, create_public_channel):
    '''
    Error Raised:
        Input Error: start is greater than the total number of messages in the channel
    Explanation:
        Currently no messages, has requested to return messages at index 1000 which does not exist
    '''
    requests.delete(config.url + 'clear/v1')
    message_response = requests.get(config.url + 'channel/messages/v2', json={
        'token': create_first_user['token'], 'channel_id': create_public_channel['channel_id'], 'start': 1000})

    assert message_response.status_code == 400


def test_unauthorised_user(create_public_channel, create_second_user):
    '''
    Error Raised:
        Input Error: channel_id is valid and the authorised user is not a member of the channel
    Explanation:
        Messages are requested by user2, who has no access to the server created by user1
    '''
    requests.delete(config.url + 'clear/v1')
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': create_second_user['token'], 'channel_id': create_public_channel['channel_id'], 'start': 0})

    assert message_response.status_code == 403


# messages send v1
def test_send_invalid_channel(create_first_user, create_public_channel):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel    
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    requests.delete(config.url + 'clear/v1')
    message = "hello"
    send_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_first_user['token'], 'channel_id': create_public_channel['channel_id'] + 1, 'message': message})

    assert send_response.status_code == 400


def test_send_invalid_message(create_first_user, create_public_channel, generate_invalid_message):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel    
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    requests.delete(config.url + 'clear/v1')
    message = generate_invalid_message
    message_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_first_user['token'], 'channel_id': create_public_channel['channel_id'], 'message': message})

    assert message_response.status_code == 400


def test_send_unauthorised_user(create_public_channel, create_second_user):
    '''
    Error Raised:
        Input Error: channel_id is valid and the authorised user is not a member of the channel
    Explanation:
        Messages are requested by user2, who has no access to the server created by user1
    '''
    requests.delete(config.url + 'clear/v1')
    message = "hello"
    send_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_second_user['token'], 'channel_id': create_public_channel['channel_id'], 'message': message})

    assert send_response.status_code == 403


# messagesedit v1
def test_edit_invalid_message(create_first_user, send_first_message, generate_invalid_message):
    '''
    Error Raised:
        Input Error: length of message is over 1000 characters
    Explanation:
        New_message is 1500 character string that is randomly generated
    '''
    requests.delete(config.url + 'clear/v1')
    new_message = generate_invalid_message
    edit_response = requests.put(config.url + 'message/edit/v1', json={
        'token': create_first_user['token'], 'message_id': send_first_message, 'message': new_message})

    assert edit_response.status_code == 400


def test_edit_invalid_message_id(create_first_user, send_first_message):
    '''
    Error Raised:
        Input Error: message_id does not refer to a valid message within a channel/DM that the authorised user has joined    
    Explanation:
        Accessing send_first_message + 1 which is not a valid id
    '''
    requests.delete(config.url + 'clear/v1')
    new_message = "hello"
    edit_response = requests.put(config.url + 'message/edit/v1', json={
        'token': create_first_user['token'], 'message_id': send_first_message + 1, 'message': new_message})

    assert edit_response.status_code == 400


def test_send_invalid_channel(create_second_user, send_first_message):
    '''
    Error Raised:
        Input Error: Message_id is valid, user is not authorised and does not have owner permissions    
    Explanation:
        Second user tries to edit, has no owner and is not the original sender of message
    '''
    requests.delete(config.url + 'clear/v1')
    new_message = "hello"
    edit_response = requests.put(config.url + 'message/edit/v1', json={
        'token': create_second_user['token'], 'message_id': send_first_message, 'message': new_message})

    assert edit_response.status_code == 403

# messages remove v1


def test_remove_invalid_message_id(create_first_user, send_first_message):
    '''
    Error Raised:
        Input Error: message_id does not refer to a valid message within a channel/DM that the authorised user has joined    
    Explanation:
        Accessing send_first_message + 1 which is not a valid id
    '''
    requests.delete(config.url + 'clear/v1')
    new_message = "hello"
    edit_response = requests.delete(config.url + 'message/remove/v1', json={
        'token': create_first_user['token'], 'message_id': send_first_message + 1, 'message': new_message})

    assert edit_response.status_code == 400


def test_remove_invalid_channel(create_second_user, send_first_message):
    '''
    Error Raised:
        Input Error: Message_id is valid, user is not authorised and does not have owner permissions    
    Explanation:
        Second user tries to edit, has no owner and is not the original sender of message
    '''
    requests.delete(config.url + 'clear/v1')
    new_message = "hello"
    edit_response = requests.delete(config.url + 'message/remove/v1', json={
        'token': create_second_user['token'], 'message_id': send_first_message, 'message': new_message})

    assert edit_response.status_code == 403
