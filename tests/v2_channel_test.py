# HTTP tests for v2 channel.py
import pytest
import requests
import json
from src import config

def test_invite():
    '''
    A simple test to check invalid channel
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    user2 = requests.post(config.url + 'auth/register/v2', params={'email' : 'email2@gmail.com', 
        'password': 'randomPassword', 'name_first' : 'First', 'name_last' : 'Last'})
    channel_1 = requests.post(config.url + 'channels/create/v2', params = {'token': user1['token'], 'name': 'First Channel', 
        'is_public': True})

    response = requests.post(config.url + 'channel/invite/v2', params={'token': user1['token'], 'channel_id': channel_1['channel_id'] + 1, 
        'u_id': user2['token']})    # don't know how to name a non existent channel id
    assert response.status_code == 400  # inputError

