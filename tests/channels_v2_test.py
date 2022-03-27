import pytest
import requests
import json
from src import config

'''test for list'''


def test_list_one_user_multiple_public_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to list all channels that are public that they are part of
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'Second Channel', 'is_public': True})

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user1_data['token']})

    assert response.status_code == 200


def test_list_one_user_multiple_mixed_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to list all channels that are public and private that they are part of
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'Second Channel', 'is_public': False})

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user1_data['token']})

    assert response.status_code == 200


def test_list_multiple_users_multiple_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 and User 2 is able to list all channels that are public and private that they are part of
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'],
                                                           'name': 'Second Channel', 'is_public': False})

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user1_data['token']})

    assert response.status_code == 200

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user2_data['token']})

    assert response.status_code == 200



def test_list_user_no_channel():
    '''
    Error raised:
        None
    Explanation:
        User 1 is list no channels as they are not part of any
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user2_data['token']})

    assert response.status_code == 200


'''test for listall'''


def test_listall_one_user_multiple_public_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to list all channels that are public 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'Second Channel', 'is_public': True})

    response = requests.get(
        config.url + 'channels/listall/v2', params={'token': user1_data['token']})

    assert response.status_code == 200


def test_listall_one_user_multiple_mixed_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to list all channels that are public and private
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'Second Channel', 'is_public': False})

    response = requests.get(
        config.url + 'channels/listall/v2', params={'token': user1_data['token']})

    assert response.status_code == 200


def test_listall_multiple_users_multiple_channels():
    '''
    Error raised:
        None
    Explanation:
        User 1 and User 2 is able to list all channels 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'],
                                                           'name': 'Second Channel', 'is_public': False})

    response = requests.get(
        config.url + 'channels/listall/v2', params={'token': user1_data['token']})

    assert response.status_code == 200

    response = requests.get(
        config.url + 'channels/listall/v2', params={'token': user2_data['token']})

    assert response.status_code == 200


def test_listall_user_no_channel():
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to list no channels, as no channels created in Seams
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'Second Channel', 'is_public': False})

    response = requests.get(
        config.url + 'channels/listall/v2', params={'token': user2_data['token']})

    assert response.status_code == 200


'''test for create'''


def test_create_invalid_channel_name_greater_than_20():
    '''
    Error raised:
        InputError: Make sure channel name no less than 1 character and no more than 20
    Explanation:
        The name of the channel is longer than 20 characters
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                      'name': 'abcdefghijklmnopqrstuvwxyz', 'is_public': True})

    assert response.status_code == 400


def test_create_invalid_channel_name_less_than_1():
    '''
    Error raised:
        InputError: 'Make sure channel name no less than 1 character and no more than 20'
    Explanation:
        The name of the channel is shorter than 1 character
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                      'name': '', 'is_public': True})

    assert response.status_code == 400


def test_create_valid_response_code():
    '''
    Error raised:
        None
    Explanation:
        All the parameters is correct and the channel creation is successful 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                      'name': 'First Channel', 'is_public': True})

    assert response.status_code == 200
