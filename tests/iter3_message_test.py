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
    
''' tests for search/v1 '''
def test_search_query_invalid_length(create_first_user):

    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})  
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})  
    
    search_response = requests.get(config.url + 'search/v1', params = {'token': user1['token'], 'query_str': ''})

    assert search_response.status_code == 400


def test_search_query_success(create_first_user):

    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is random'})  
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message 1'})    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message 2'})  
    
    search_response = requests.get(config.url + 'search/v1', params = {'token': user1['token'], 'query_str': 'message'})

    assert search_response.status_code == 200
    
def test_search_query_user_not_joined_any_dms_nor_channels(create_first_user):

    user1 = create_first_user
    search_response = requests.get(config.url + 'search/v1', params = {'token': user1['token'], 'query_str': 'message'})
    response_data = search_response.json()

    assert search_response.status_code == 200
    assert response_data == {'messages':[]}

def test_search_multiple_dms(create_first_user):
    user1 = create_first_user
    dm_response1 = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data1 = dm_response1.json()
    dm_response2 = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data2 = dm_response2.json()
    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data2['dm_id'], 'message': 'this is random'})  
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data1['dm_id'], 'message': 'this is a message 1'})    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data2['dm_id'], 'message': 'this is a message 2'})  
    
    search_response = requests.get(config.url + 'search/v1', params = {'token': user1['token'], 'query_str': 'message'})

    assert search_response.status_code == 200

def test_search_is_user_reacted(create_first_user):
    user1 = create_first_user

    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()    
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})
    search_response = requests.get(config.url + 'search/v1', params = {'token': user1['token'], 'query_str': 'message'})

    assert search_response.status_code == 200

''' tests for message/react/v1 '''
def test_react_invalid_message_id(create_first_user):

    user1 = create_first_user
    
    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()
      
    resp = requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'] + 1, 'react_id': 1})
    
    assert resp.status_code == 400

def test_react_invalid_react_id(create_first_user):
    
    user1 = create_first_user
    
    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json() 
    
    resp = requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 2})       

    assert resp.status_code == 400
    
def test_react_already_reacted(create_first_user):

    user1 = create_first_user

    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()    
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})  

    resp = requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})   

    assert resp.status_code == 400
    
def test_react_success(create_first_user):
    
    user1 = create_first_user

    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()    
    
    resp = requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})
        
    assert resp.status_code == 200
    
    
''' tests for message/unreact/v1 '''
def test_unreact_invalid_message_id(create_first_user):
    user1 = create_first_user
    
    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()
      
    resp = requests.post(config.url + 'message/unreact/v1', json = {'token': user1['token'], 'message_id': message['message_id'] + 1, 'react_id': 1})
    
    assert resp.status_code == 400


def test_unreact_invalid_react_id(create_first_user):
    user1 = create_first_user
    
    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json() 
    
    resp = requests.post(config.url + 'message/unreact/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 2})       

    assert resp.status_code == 400   
    
def test_unreact_never_reacted(create_first_user):
    user1 = create_first_user

    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()    
    
    resp = requests.post(config.url + 'message/unreact/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})   

    assert resp.status_code == 400   

    
def test_unreact_success(create_first_user):
    user1 = create_first_user

    channel_data = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'],
                                                                       'name': 'First Channel', 'is_public': True})
    channel = channel_data.json()

    message_data = requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel['channel_id'], 'message': 'This is a message'})
    message = message_data.json()    
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})  

    resp = requests.post(config.url + 'message/unreact/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})   

    assert resp.status_code == 200
  
    
    
