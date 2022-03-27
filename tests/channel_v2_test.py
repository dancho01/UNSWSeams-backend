import pytest
import requests
import random
import string
import json
from src import config


@pytest.fixture
def create_first_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    return user1_data


@pytest.fixture
def create_second_user():
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                                                 'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2_data = user2.json()
    print("create second user")
    print(user2_data)
    return user2_data


@pytest.fixture
def create_public_channel():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    print(user1_data)
    c1 = requests.post(config.url + 'channels/create/v2',
                       json={'token': user1_data['token'], 'name': 'ch1', 'is_public': True})
    channel1 = c1.json()
    print(channel1)

    return channel1, user1_data


@pytest.fixture
def generate_invalid_message():
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(1500))
    return invalid_message


@pytest.fixture
def send_first_message():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password123",
        "name_first": "first",
        "name_last": "last"
    })
    user1_data = user1.json()
    c1 = requests.post(config.url + 'channels/create/v2',
                       json={'token': user1_data['token'], 'name': 'ch1', 'is_public': True})
    channel1 = c1.json()
    response = requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel1['channel_id'], 'message': "hello"})
    message_response = response.json()
    return message_response, user1_data, channel1


'''
 messages v2
'''


def test_messages_invalid_channel(create_public_channel):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': create_public_channel[1]['token'], 'channel_id': create_public_channel[0]['channel_id'] + 1, 'start': 0})

    assert message_response.status_code == 400


def test_invalid_start(create_public_channel):
    '''
    Error Raised:
        Input Error: start is greater than the total number of messages in the channel
    Explanation:
        Currently no messages, has requested to return messages at index 1000 which does not exist
    '''
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': create_public_channel[1]['token'], 'channel_id': create_public_channel[0]['channel_id'], 'start': 1000})
    assert message_response.status_code == 400


def test_unauthorised_user(create_public_channel, create_second_user):
    '''
    Error Raised:
        Input Error: channel_id is valid and the authorised user is not a member of the channel
    Explanation:
        Messages are requested by user2, who has no access to the server created by user1
    '''
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': create_second_user['token'], 'channel_id': create_public_channel[0]['channel_id'], 'start': 0})

    assert message_response.status_code == 403


'''
messages send v1
'''


def test_send_invalid_channel(create_public_channel):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    message = "hello"
    send_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_public_channel[1]['token'], 'channel_id': create_public_channel[0]['channel_id'] + 1, 'message': message})

    assert send_response.status_code == 400


def test_send_invalid_message(create_public_channel, generate_invalid_message):
    '''
    Error Raised:
        Input Error: channel_id does not refer to a valid channel
    Explanation:
        Passing in create_public_channel['channel_id'] + 1, which is invalid
    '''
    message = generate_invalid_message
    message_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_public_channel[1]['token'], 'channel_id': create_public_channel[0]['channel_id'], 'message': message})

    assert message_response.status_code == 400


def test_send_unauthorised_user(create_public_channel, create_second_user):
    '''
    Error Raised:
        Input Error: channel_id is valid and the authorised user is not a member of the channel
    Explanation:
        Messages are requested by user2, who has no access to the server created by user1
    '''
    message = "hello"
    send_response = requests.post(config.url + 'message/send/v1', json={
        'token': create_second_user['token'], 'channel_id': create_public_channel[0]['channel_id'], 'message': message})

    assert send_response.status_code == 403
    
    
def test_send_message_success():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})
    channel_response = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'Second Channel', 'is_public' : True})

    channel_data = channel_response.json()
            
    message_response = requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
            

    assert message_response.status_code == 200 


'''
messages edit v1
'''


def test_edit_invalid_message(send_first_message, generate_invalid_message):
    '''
    Error Raised:
        Input Error: length of message is over 1000 characters
    Explanation:
        New_message is 1500 character string that is randomly generated
    '''
    new_message = generate_invalid_message
    edit_response = requests.put(config.url + 'message/edit/v1', json={
        'token': send_first_message[1]['token'], 'message_id': send_first_message[0]['message_id'], 'message': new_message})

    assert edit_response.status_code == 400


def test_edit_invalid_message_id(send_first_message):
    '''
    Error Raised:
        Input Error: message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    Explanation:
        Accessing send_first_message + 1 which is not a valid id
    '''
    new_message = "hello"
    edit_response = requests.put(config.url + 'message/edit/v1', json={
        'token': send_first_message[1]['token'], 'message_id': send_first_message[0]['message_id'] + 1, 'message': new_message})

    assert edit_response.status_code == 400
    
    
def test_edit_message_unauthorised():

    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})
    dm_data = dm_response.json()
    
    message_response = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a message'})
            
    message_data = message_response.json()

    edit_response = requests.put(config.url + 'message/edit/v1', json = {'token' : user2_data['token'], 
            'message_id' : message_data['message_id'], 'message': 'updated message'})

    assert edit_response.status_code == 403    


def test_edit_empty_string():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []})
    dm_data = dm_response.json()
    
    message_response = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a message'})
            
    message_data = message_response.json()

    edit_response = requests.put(config.url + 'message/edit/v1', json = {'token' : user1_data['token'], 
            'message_id' : message_data['message_id'], 'message': ''})

    assert edit_response.status_code == 200  


def test_edit_message_channel_success():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_1_data = channel_1.json()
    
    requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
            
    message_response = requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_1_data['channel_id'], 'message': 'This is a second message'})
            
    message_data = message_response.json()

    edit_response = requests.put(config.url + 'message/edit/v1', json = {'token' : user1_data['token'], 
            'message_id' : message_data['message_id'], 'message': 'This is updated'})

    assert edit_response.status_code == 200  
    
    
def test_edit_message_dm_success():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []})
    dm_data = dm_response.json()
    
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a message'})
        
    message_response = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a second message'})
            
    message_data = message_response.json()

    edit_response = requests.put(config.url + 'message/edit/v1', json = {'token' : user1_data['token'], 
            'message_id' : message_data['message_id'], 'message': 'This is updated'})

    assert edit_response.status_code == 200  

# def test_edit_invalid_channel(send_first_message, create_second_user):
#     '''
#     Error Raised:
#         Access Error: channel_id is valid and the authorised user is not a member of the channel
#     Explanation:
#         Second user tries to edit, has no owner and is not the original sender of message
#     '''
#     new_message = "hello"
#     edit_response = requests.put(config.url + 'message/edit/v1', json={
#         'token': create_second_user['token'], 'message_id': send_first_message[0]['message_id'], 'message': new_message})

#     assert edit_response.status_code == 403

"""
test when message changed to empty string deletes the message
"""

"""
test message is edited and outputs correctly

"""



'''
messages remove v1
'''


def test_remove_invalid_message_id(send_first_message):
    '''
    Error Raised:
        Input Error: message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    Explanation:
        Accessing send_first_message + 1 which is not a valid id
    '''
    new_message = "hello"
    edit_response = requests.delete(config.url + 'message/remove/v1', json={
        'token': send_first_message[1]['token'], 'message_id': send_first_message[0]['message_id'] + 1, 'message': new_message})

    assert edit_response.status_code == 400
    
def test_message_remove_unauthorised():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_1_data = channel_1.json()
    
    requests.post(config.url + 'channel/join/v2', json = {'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
     
    message_response = requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
            
    message_data = message_response.json()

    removal_response = requests.delete(config.url + 'message/remove/v1', json = {'token' : user2_data['token'], 'message_id' : message_data['message_id']})

    assert removal_response.status_code == 403     
    
    
def test_message_remove_channel_success():   
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})

    channel_1_data = channel_1.json()
    
    requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
    
    message_response = requests.post(config.url + 'message/send/v1', json = {'token': user1_data['token'], 
            'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
            
    message_data = message_response.json()

    removal_response = requests.delete(config.url + 'message/remove/v1', json = {'token' : user1_data['token'], 'message_id' : message_data['message_id']})

    assert removal_response.status_code == 200   
    
    
def test_message_remove_dm_success():
    requests.delete(config.url + 'clear/v1' )

    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})
    
    user1_data = user1.json()

    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': []})
    dm_data = dm_response.json()
        
    requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a message'})
    
    message_response = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'], 
            'dm_id': dm_data['dm_id'], 'message': 'This is a message'})
            
    message_data = message_response.json()

    removal_response = requests.delete(config.url + 'message/remove/v1', json = {'token' : user1_data['token'], 'message_id' : message_data['message_id']})

    assert removal_response.status_code == 200 


# def test_remove_invalid_channel(send_first_message):
#     '''
#     Error Raised:
#         Input Error: Message_id is valid, user is not authorised and does not have owner permissions
#     Explanation:
#         Second user tries to edit, has no owner and is not the original sender of message
#     '''
#     edit_response = requests.delete(config.url + 'message/remove/v1', json={
#         'token': send_first_message[1]['token'], 'message_id': send_first_message[0]['message_id']})

#     assert edit_response.status_code == 403

'''test for channel_details_v2'''


def test_channel_detail_one_channel_success():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                       'name': 'First Channel', 'is_public': True})

    channel_1_data = channel_1.json()

    response = requests.get(config.url + 'channel/details/v2', params={
                            'token': user1_data['token'], 'channel_id': channel_1_data['channel_id']})

    assert response.status_code == 200


def test_channel_detail_invalid_channel():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                       'name': 'First Channel', 'is_public': True})

    channel_1_data = channel_1.json()

    response = requests.get(config.url + 'channel/details/v2', params={
                            'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1})

    assert response.status_code == 400


def test_channel_detail_invalid_user():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                       'name': 'First Channel', 'is_public': True})

    channel_1_data = channel_1.json()

    response = requests.get(config.url + 'channel/details/v2', params={
                            'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})

    assert response.status_code == 403
<<<<<<< HEAD
    
    
''' tests for channel/leave/v1 '''
def test_channel_leave_invalid_channel():
    requests.delete(config.url + 'clear/v1' ) 
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()
    
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})
    
    channel_1_data = channel_1.json()
    
    response = requests.post(config.url + 'channel/leave/v1', json = {'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'] + 1})
    
    assert response.status_code == 400
    
    
def test_channel_leave_not_member():
    requests.delete(config.url + 'clear/v1' ) 
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'EMAIL@gmail.com', 
    'password' : 'password1', 'name_first' : 'FIRST', 'name_last' : 'LAST'})

    user2_data = user2.json()
    
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})
    
    channel_1_data = channel_1.json()
    
    response = requests.post(config.url + 'channel/leave/v1', json = {'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    
    assert response.status_code == 403
        
    
def test_channel_leave_success():
    requests.delete(config.url + 'clear/v1' ) 
    
    user1 = requests.post(config.url + 'auth/register/v2', json = {'email' : 'email@gmail.com', 
    'password' : 'password', 'name_first' : 'First', 'name_last' : 'Last'})

    user1_data = user1.json()
    
    channel_1 = requests.post(config.url + 'channels/create/v2', json = {'token' : user1_data['token'], 
    'name' : 'First Channel', 'is_public' : True})
    
    channel_1_data = channel_1.json()
    
    response = requests.post(config.url + 'channel/leave/v1', json = {'token': user1_data['token'], 'channel_id': channel_1_data['channel_id']})
    
    assert response.status_code == 200    
    
    
    


=======
>>>>>>> f973d98bf9e02b3bcef3039fbfa878bd1cb90d49
