import pytest
import requests
import json
from src import config 

''' fixtures '''

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


''' tests for dm/create/v1'''

def test_dm_create_invalid_u_ids(create_first_user):

    user = create_first_user  
     
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user['token'] , 'u_ids': [user['auth_user_id'] + 1]})
    
    assert dm_response.status_code == 400
   
    
def test_dm_create_duplicate_u_ids(create_first_user, create_second_user):

    user1 = create_first_user
    user2 = create_second_user   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id'], user2['auth_user_id']]})  
     
    assert dm_response.status_code == 400 
    
    
def test_dm_create_success(create_first_user, create_second_user):

    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})   
    
    assert dm_response.status_code == 200
    
    
''' tests for dm/list/v1 ''' 

def test_dm_list_success(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user
    
    requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})  
    requests.post(config.url + 'dm/create/v1', json = {'token': user2['token'] , 'u_ids': [user1['auth_user_id']]})  
    requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []})  
    
    dm_list = requests.get(config.url + 'dm/list/v1', params = {'token': user1['token']})
    
    assert dm_list.status_code == 200
 
 
def test_dm_list_success_no_dms(create_first_user):
    
    user1 = create_first_user  
    
    dm_list = requests.get(config.url + 'dm/list/v1', params = {'token': user1['token']})
    
    assert dm_list.status_code == 200

    
    
''' tests for dm/remove/v1 '''
def test_dm_remove_invalid_dm(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_remove.status_code == 400
    
    
def test_dm_remove_not_owner(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user    

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
       
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})    
    
    assert dm_remove.status_code == 403
    
    
def test_dm_remove_owner_already_left(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user
    
    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
    
    requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})  
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_remove.status_code == 403  
    
    
def test_dm_remove_success_case(create_first_user):  

    user1 = create_first_user

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm.json()  
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']}) 
    
    assert dm_remove.status_code == 200   
    
    
    
''' tests for dm/details/v1 '''
def test_dm_details_invalid_dm(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_details.status_code == 400
    
    
def test_dm_details_user_not_member(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_details.status_code == 403
    
    
def test_dm_details_success(create_first_user):
    
    user1 = create_first_user   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
   
    assert dm_details.status_code == 200
   
       
''' tests for dm/leave/v1 '''
def test_dm_leave_invalid_dm(create_first_user):
    
    user1 = create_first_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_leave.status_code == 400
    
    
def test_dm_leave_user_not_member(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_leave.status_code == 403
    
    
def test_dm_leave_success(create_first_user):

    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_leave.status_code == 200
    
    
''' tests for dm/messages/v1 '''
def test_dm_messages_invalid_dm(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1, 'start': 0})
    
    assert dm_messages.status_code == 400
    
    
def test_dm_messages_invalid_start(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'start': 10})
    
    assert dm_messages.status_code == 400
    
    
def test_dm_messages_user_not_member(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user2['token'] , 'dm_id': dm_data['dm_id'], 'start': 0})
    
    assert dm_messages.status_code == 403
    
    
def test_dm_return_messages_success(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is message 1'})
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is message 2'})        
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is message 3'})
        
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'start': 1})
    
    assert dm_messages.status_code == 200    
    
    
''' tests for message/senddm/v1 '''
def test_dm_send_message_invalid_dm(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1, 'message': 'this is a message'})
    
    assert dm_sent.status_code == 400
    
    
def test_dm_send_message_invalid_length(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': ''})
    
    assert dm_sent.status_code == 400   
    
    
def test_dm_send_message_user_not_member(create_first_user, create_second_user):
    
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})
    
    assert dm_sent.status_code == 403     
    

def test_dm_send_message_success(create_first_user):
    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})    

    assert dm_sent.status_code == 200




      
