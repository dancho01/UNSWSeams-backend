import requests
import pytest
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


'''test for user_profile_v1'''


def test_valid_user():
    '''
    Error raised:
        None
    Explanation:
        User 1's u_id is valid 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params={
                            'token': user1_data['token'], 'u_id': user1_data['auth_user_id']})

    assert response.status_code == 200


def test_invalid_user():
    '''
    Error raised:
        InputError: u_id does not refer to a valid user
    Explanation:
        User 1's u_id is invalid 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params={
                            'token': user1_data['token'], 'u_id': user1_data['auth_user_id'] + 1})

    assert response.status_code == 400


'''
<<<<<<< HEAD
user/stats test

'''

# test number of messages after removing messages
def test_user_stats_total_num_messages_after_removing_messages():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})

    channel_data = channel_response.json()

    message_response = requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    
    message_data = message_response.json()

    requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})


    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert response_data['user_stats']['channels_joined'][2]['num_channels_joined'] == 2
    assert type(response_data['user_stats']['channels_joined'][2]['time_stamp']) == int
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 0
    
    # {
    #     'user_stats': {
    #         'channels_joined': [
    #             {
    #                 'num_channels_joined': 0,
    #                 'time_stamp': 0
    #             }, 
    #             {
    #                 'num_channels_joined': 1,
    #                 'time_stamp': 23456789
    #             }
    #         ],
    #         'dms_joined': [
    #             {
    #                 'num_dms_joined': 0,
    #                 'time_stamp': 0
    #             },
    #             {
    #                 'num_dms_joined': 1,
    #                 'time_stamp': 987654
    #             }
    #         ],
    #         'messages_sent': [
    #             {
    #                 'num_msgs_sent': 0,
    #                 'time_stamp': 0
    #             }, 
    #             {
    #                 'num_msgs_sent': 1,
    #                 'time_stamp': 1234590
    #             }
    #         ],
    #         'involvement_rate': 0.0
    #     }
    # }

'''
users/stats test

'''

# test number of messages after removing messages
def test_users_stats_total_num_messages_after_removing_messages():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    user2_data = user2.json()

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})

    channel_data = channel_response.json()

    message_response = requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    
    message_data = message_response.json()

    requests.post(config.url + 'channel/join/v2',
                  json={'token': user2_data['token'], 'channel_id': channel_data['channel_id']})

    requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})


    response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})

    assert response.status_code == 200
    # assert response_data = {}

'''
    test for notifications
'''


def test_valid_notification(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 invites user 2, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()

    assert len(response_receiver_data['notifications']) == 1
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

