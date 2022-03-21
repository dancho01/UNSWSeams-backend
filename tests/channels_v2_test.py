import pytest
import requests
import json
from src import config

'''test for list'''

def test_0_one_user_multiple_public_channels():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : True})

    response = requests.get(config.url + 'channels/list/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

def test_1_one_user_multiple_mixed_channels():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : False})

    response = requests.get(config.url + 'channels/list/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

    # assert json.loads(response.text) == {'channels': [{'channel_id' : channel_1['channel_id'], 'name' : 'First Channel'},
    # {'channel_id' : channel_2['channel_id'], 'name' : 'Second Channel'}]}

def test_2_multiple_users_multiple_channels():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user2_data['token'], 
    'name' : 'Second Channel', 'is_public' : False})

    response = requests.get(config.url + 'channels/list/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

    # assert json.loads(response.text) == {'channels': [{'channel_id' : channel_1['channel_id'], 'name' : 'First Channel'}]}

    response = requests.get(config.url + 'channels/list/v2', params = {'token' : user2_data['token']})

    assert response.status_code == 200

    # assert json.loads(response.text) == {'channels': [{'channel_id' : channel_2['channel_id'], 'name' : 'Second Channel'}]}

def test_3_user_no_channel():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    response = requests.get(config.url + 'channels/list/v2', params = {'token' : user2_data['token']})

    assert response.status_code == 200



'''test for listall'''

def test_0_one_user_multiple_public_channels():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : True})

    response = requests.get(config.url + 'channels/listall/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

def test_1_one_user_multiple_mixed_channels():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : False})

    response = requests.get(config.url + 'channels/listall/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

def test_2_multiple_users_multiple_channels():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user2_data['token'], 
    'name' : 'Second Channel', 'is_public' : False})

    response = requests.get(config.url + 'channels/listall/v2', params = {'token' : user1_data['token']})

    assert response.status_code == 200

    # assert json.loads(response.text) == {'channels': [{'channel_id' : channel_1['channel_id'], 'name' : 'First Channel'}]}

    response = requests.get(config.url + 'channels/listall/v2', params = {'token' : user2_data['token']})

    assert response.status_code == 200


def test_3_user_no_channel():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_2 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : False})

    response = requests.get(config.url + 'channels/listall/v2', params = {'token' : user2_data['token']})

    assert response.status_code == 200;

'''test for create'''

def test_invalid_channel_name_greater_than_20():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    response = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'abcdefghijklmnopqrstuvwxyz', 'is_public' : True})
        
    assert response.status_code == 400;

def test_invalid_channel_name_less_than_1():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    response = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : '', 'is_public' : True})
        
    assert response.status_code == 400;

def test_valid_response_code():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()
        
    response = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    assert response.status_code == 200;
