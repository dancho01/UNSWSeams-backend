import pytest
import requests
import json
from src import config 
from src.data_store import data_store, return_member_information, check_user_registered

'''test for user_profile_v1'''

def test_valid_user():
    requests.delete(config.url + 'clear/v1')   

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params = {'token' : user1_data['token'], 'u_id' : user1_data['auth_user_id']})

    assert response.status_code == 200

def test_invalid_user():
    requests.delete(config.url + 'clear/v1')   

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params = {'token' : user1_data['token'], 'u_id' : user1_data['auth_user_id'] + 1})

    assert response.status_code == 400
