import pytest
import requests
import json
from src import config 

'''tests for users all'''

def test_one_user():
    requests.delete(config.url + 'clear/v1')   

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()
 
    response = requests.get(config.url + 'users/all/v1', params = {'token' : user1_data['token']})

    assert response.status_code == 200

def test_multiple_users():
    requests.delete(config.url + 'clear/v1')   

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    
    requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user1_data = user1.json()

    response = requests.get(config.url + 'users/all/v1', params = {'token' : user1_data['token']})

    assert response.status_code == 200
