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
    '''
    Error raised:
        InputError: any u_id in u_ids does not refer to a valid user
    Explanation:
        Passing in an invalid user id as there is only one user, however, it 
        has passed in (u_id + 1), which doesn't exist
    '''
    user = create_first_user  
     
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user['token'] , 'u_ids': [user['auth_user_id'] + 1]})
    
    assert dm_response.status_code == 400
   
    
def test_dm_create_duplicate_u_ids(create_first_user, create_second_user):
    '''
    Error raised: 
        InputError: there are duplicate 'u_id's in u_ids
    Explanation:
        the u_id of user2 is being passed in twice, throwing an Input error
    '''
    user1 = create_first_user
    user2 = create_second_user   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id'], user2['auth_user_id']]})  
     
    assert dm_response.status_code == 400 
    
    
def test_dm_create_success(create_first_user, create_second_user):
    '''
    Error raised:
        None
    Explanation:
        There are no errors thrown and the dm is succesfully created
    '''
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})   
    
    assert dm_response.status_code == 200
    
    
''' tests for dm/list/v1 ''' 

def test_dm_list_success(create_first_user, create_second_user):
    '''
    Error raised:
        None
    Explanation:
        Succesfully returns a list of all the DMs that the user is member of 
    '''    
    user1 = create_first_user
    user2 = create_second_user
    
    requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})  
    requests.post(config.url + 'dm/create/v1', json = {'token': user2['token'] , 'u_ids': [user1['auth_user_id']]})  
    requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []})  
    
    dm_list = requests.get(config.url + 'dm/list/v1', params = {'token': user1['token']})
    
    assert dm_list.status_code == 200
 
 
def test_dm_list_success_no_dms(create_first_user):
    '''
    Error raised:
        None
    Explanation:
        When a user is not a member of any DM, it just returns an empty list   
    '''    
    user1 = create_first_user  
    
    dm_list = requests.get(config.url + 'dm/list/v1', params = {'token': user1['token']})
    
    assert dm_list.status_code == 200

    
    
''' tests for dm/remove/v1 '''
def test_dm_remove_invalid_dm(create_first_user, create_second_user):
    '''
    Error raised:
        InputError: dm_id does not refer to a valid DM
    Explanation: 
        The dm_id passed in is invalid as 1 is added to the only dm_id that exists       
    '''    
    user1 = create_first_user
    user2 = create_second_user

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_remove.status_code == 400
    
    
def test_dm_remove_not_owner(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is not the original DM creator
    Explanation: 
        An error is thrown as user 2 is not an owner and only the original creators 
        of the DM can remove DMs
    '''   
    user1 = create_first_user
    user2 = create_second_user    

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
       
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})    
    
    assert dm_remove.status_code == 403
    
    
def test_dm_remove_owner_already_left(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is no longer in the DM
    Explanation:
        User 1, who is the original creator of the DM, leaves the channel, and is
        no longer able to remove the DM              
    '''       
    user1 = create_first_user
    user2 = create_second_user
    
    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm.json()
    
    requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})  
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_remove.status_code == 403  
    
 
    
def test_dm_remove_success_case(create_first_user):  
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to succesfully remove the DM as he is the original creator
    '''   
    user1 = create_first_user

    dm = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm.json()  
    
    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']}) 
    
    assert dm_remove.status_code == 200   
    
    
    
''' tests for dm/details/v1 '''
def test_dm_details_invalid_dm(create_first_user, create_second_user):
    '''
    Error raised:
        InputError: dm_id does not refer to a valid DM
    Explanation:
        The dm_id passed in is invalid as 1 is added to the only dm_id that exists                 
    '''    
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_details.status_code == 400
   
    
    
def test_dm_details_user_not_member(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is not a member of the DM
    Explanation:
        User 2 is not a member of the DM with the given dm_id and so throws an AccessError     
    '''   
    user1 = create_first_user
    user2 = create_second_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_details.status_code == 403
    
  
    
def test_dm_details_success(create_first_user):
    '''
    Error raised:
        None
    Explanation:
        Dm details are succesfully provided to user 1, as he is a member of the DM
    '''   
    user1 = create_first_user   
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_details = requests.get(config.url + 'dm/details/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
   
    assert dm_details.status_code == 200
   
 
       
''' tests for dm/leave/v1 '''
def test_dm_leave_invalid_dm(create_first_user):
    '''
    Error raised:
        InputError: dm_id does not refer to a valid DM
    Explanation:
        The dm_id passed in is invalid as 1 is added to the only dm_id that exists  
    '''   
    user1 = create_first_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1})
    
    assert dm_leave.status_code == 400
    
 
    
def test_dm_leave_user_not_member(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is not a member of the DM
    Explanation:
        User 2 is not a member of the DM with the given dm_id and so throws an AccessError         
    '''   
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_leave.status_code == 403
    

    
def test_dm_leave_success(create_first_user):
    '''
    Error raised:
        None
    Explanation:
        User 1 is able to succesfully leave the DM and is removed as a member of the DM   
    '''
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id']})
    
    assert dm_leave.status_code == 200
 
    
    
''' tests for dm/messages/v1 '''
def test_dm_messages_invalid_dm(create_first_user):
    '''
    Error raised:
        InputError: dm_id does not refer to a valid DM
    Explanation:
        The dm_id passed in is invalid as 1 is added to the only dm_id that exists      
    '''   
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1, 'start': 0})
    
    assert dm_messages.status_code == 400
    
  
    
def test_dm_messages_invalid_start(create_first_user):
    '''
    Error raised:
        InputError: start is greater than the total number of messages in the DM
    Explanation:
        An error is thrown as the starting index of when to return messages is 
        greater than the total number of messages
    '''    
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'start': 10})
    
    assert dm_messages.status_code == 400
    
  
    
def test_dm_messages_user_not_member(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is not a member of the DM
    Explanation:
        User 2 is not a member of the DM with the given dm_id and so throws an AccessError                
    '''  
    user1 = create_first_user
    user2 = create_second_user  
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_messages = requests.get(config.url + 'dm/messages/v1', params = {'token': user2['token'] , 'dm_id': dm_data['dm_id'], 'start': 0})
    
    assert dm_messages.status_code == 403
    

    
def test_dm_return_messages_success(create_first_user):
    '''
    Error raised:
        None
    Explanation:
        Succesfully returns up to 50 messages between the "start" index and "start + 50"
        In this case, returns the messages with index 1 and 2
    '''  
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
    '''
    Error raised:
        InputError: dm_id does not refer to a valid DM
    Explanation:
        The dm_id passed in is invalid as 1 is added to the only dm_id that exists      
    '''   
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'] + 1, 'message': 'this is a message'})
    
    assert dm_sent.status_code == 400
    
   
    
def test_dm_send_message_invalid_length(create_first_user):
    '''
    Error raised:
        InputError: length of message is less than 1 or over 1000 characters
    Explanation:
        An error is raised as the message inputed has 0 characters    
    '''   
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': ''})
    
    assert dm_sent.status_code == 400   
    
    
    
def test_dm_send_message_user_not_member(create_first_user, create_second_user):
    '''
    Error raised:
        AccessError: dm_id is valid and the authorised user is not a member of the DM
    Explanation:
        User 2 is not a member of the DM with the given dm_id and so throws an AccessError                     
    '''   
    user1 = create_first_user
    user2 = create_second_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})
    
    assert dm_sent.status_code == 403     
    


def test_dm_send_message_success(create_first_user):
    '''
    Error raised:
        None
    Explanation:
        A message is succesfully sent to the dm by the user and no errors are
        thrown
    ''' 
    user1 = create_first_user
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': []}) 
    dm_data = dm_response.json()
    
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is a message'})    

    assert dm_sent.status_code == 200




      
