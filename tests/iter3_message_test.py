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
    
    
    
    
