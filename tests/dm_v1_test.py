import pytest
import requests
import json
from src import config 

''' tests for dm create'''

def test_dm_create_invalid_u_ids():    
    requests.delete(config.url + 'clear/v1')   
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user1_data['auth_user_id'] + 1]})
    assert dm_response.status_code == 400
   
    
def test_dm_create_duplicate_u_ids():
    requests.delete(config.url + 'clear/v1')   
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()    
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id'], user2_data['auth_user_id']]})   
    assert dm_response.status_code == 400 
    
    
def test_dm_create_success():
    requests.delete(config.url + 'clear/v1')   
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()    
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})   
    assert dm_response.status_code == 200
    
    
''' tests for dm/list/v1 ''' 

def test_dm_list():
    requests.delete(config.url + 'clear/v1')   
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()    
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    
     
    assert dm_response.status_code == 200
    
    
''' tests for dm/remove/v1 '''
def test_dm_remove_invalid_dm():
    requests.delete(config.url + 'clear/v1')   
     
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
       
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_remove.status_code == 400
    
    
def test_dm_remove_not_owner():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' :  'seconduser@gmail.com', 
    'password' : 'password', 'name_first' : 'DifferentFirst', 'name_last' : 'DifferentLast'}) 
    user2_data = user2.json()
   
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]}) 
    dm_data = dm_response.json()    
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user2_data['token'] , 'dm_id': dm_data['dm_id']})    
    
    assert dm_remove.status_code == 403
    
    
def test_dm_remove_owner_already_removed():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
   
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()    
    
    dm_remove = requests.post(config.url + 'dm/leave/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']})
   
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']})
    assert dm_remove.status_code == 403    
    
    
''' tests for dm/details/v1 '''
def test_dm_details_invalid_dm():
    requests.delete(config.url + 'clear/v1')   
     
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_details.status_code == 400
    
    
def test_dm_details_user_not_member():
    requests.delete(config.url + 'clear/v1')   
     
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user2_data['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_details.status_code == 403
    
    
def test_dm_details_success():
    requests.delete(config.url + 'clear/v1')   
     
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()    
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']})
   
    assert dm_details.status_code == 200
   
       
''' tests for dm/leave/v1 '''
def test_dm_leave_invalid_dm():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_leave.status_code == 400
    
def test_dm_leave_user_not_member():
    requests.delete(config.url + 'clear/v1')   
     
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'anotherpassword', 'name_first' : 'Firstname', 'name_last' : 'Lastname'}) 
    user2_data = user2.json()   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user2_data['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_leave.status_code == 403
    
    
''' tests for dm/messages/v1 '''
def test_dm_messages_invalid_dm():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'] + 1, 'start': 0})
    
    assert dm_messages.status_code == 400
    
''' tests for message/senddm/v1 '''
def test_dm_send_message_invalid_dm():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'] + 1, 'message': 'this is a message'})
    
    assert dm_sent.status_code == 400
    
    
def test_dm_send_message_invalid_length():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 'message': ''})
    
    assert dm_sent.status_code == 400   
    
    
def test_dm_send_message_user_not_member():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'Differentpassword', 'name_first' : 'DifferentFirst', 'name_last' : 'DifferentLast'}) 
    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user2_data['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})
    
    assert dm_sent.status_code == 403     
    

def test_dm_send_message_success():
    requests.delete(config.url + 'clear/v1')
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'firstuser@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'}) 
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'seconduser@gmail.com', 
    'password' : 'Differentpassword', 'name_first' : 'DifferentFirst', 'name_last' : 'DifferentLast'}) 
    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})    

    assert dm_sent.status_code == 200




      
