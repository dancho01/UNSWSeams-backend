import requests
import pytest
from src import config
from src.channel_helper import time_now



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

'''test for user_profile_upload_v1'''

def test_valid_image():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://cdn.britannica.com/91/181391-050-1DA18304/cat-toes-paw-number-paws-tiger-tabby.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 200

def test_valid_image2():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 200


def test_not_valid_image_jpg():

    requests.delete(config.url + 'clear/v1')

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'Firstt', 'name_last': 'Last'})

    user2_data = user2.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_not_valid_image2_jpg():

    requests.delete(config.url + 'clear/v1')

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'Firstt', 'name_last': 'Last'})

    user2_data = user2.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.pngall.com/wp-content/uploads/2016/04/Banana-Free-Download-PNG.png', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_not_valid_url():

    requests.delete(config.url + 'clear/v1')

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'Firstt', 'name_last': 'Last'})

    user2_data = user2.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://google.com/badpage', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid_dimensions():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : -1, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid2_dimensions():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 1549, 'y_end' : 100})

    assert response.status_code == 400

def test_start_dimension_bigger():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 100, 'y_start': 0, 'x_end' : 4, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid_status_code():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'http://localhost:29499/Views/ImageOrgChart/Org_Chart.jpg', 'x_start' : 100, 'y_start': 0, 'x_end' : 4, 'y_end' : 100})

    assert response.status_code == 400

def test_valid_image_multiple_users_in_channel():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})
    
    response1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    response2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response1.status_code == 200
    assert response2.status_code == 200

def test_valid_image_multiple_users_in_dm():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'randomPassword', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()

    requests.post(
        config.url + 'dm/create/v1', json={'token': user1_data['token'], 'u_ids': [user2_data['auth_user_id']]})

    response1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})
    
    response2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response1.status_code == 200
    assert response2.status_code == 200



'''

user/stats test

'''
# test starting figures
def test_user_stats_base_case():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()

    #channels joined
    assert response.status_code == 200
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert len(response_data['user_stats']['channels_joined']) == 1
    assert type(response_data['user_stats']['channels_joined'][0]['time_stamp']) == int
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert len(response_data['user_stats']['messages_sent']) == 1
    assert type(response_data['user_stats']['messages_sent'][0]['time_stamp']) == int
    # dms joined
    assert response_data['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert len(response_data['user_stats']['dms_joined']) == 1
    assert type(response_data['user_stats']['dms_joined'][0]['time_stamp']) == int
    #involvement rate
    assert response_data['user_stats']['involvement_rate'] == 0.0
    assert type (response_data['user_stats']['involvement_rate']) == float

def test_users_stats_base_case():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()

    #channels exit
    assert response.status_code == 200
    assert response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert len(response_data['workspace_stats']['channels_exist']) == 1
    assert type(response_data['workspace_stats']['channels_exist'][0]['time_stamp']) == int
    # messages exist
    assert response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert len(response_data['workspace_stats']['messages_exist']) == 1
    assert type(response_data['workspace_stats']['messages_exist'][0]['time_stamp']) == int
    # dms exist
    assert response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(response_data['workspace_stats']['dms_exist']) == 1
    assert type(response_data['workspace_stats']['dms_exist'][0]['time_stamp']) == int
    # utilization rate
    assert response_data['workspace_stats']['utilization_rate'] == 0.0
    assert type(response_data['workspace_stats']['utilization_rate']) == float

# test number of messages after removing messages in channel & dm
def test_user_stats_users_stats_num_messages_after_removing_messages():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_data = channel_response.json()

    message_response = requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    
    message_data = message_response.json()

    requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})
    # dm - message remove
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    dm_message_data = dm_sent.json()    
    assert dm_sent.status_code == 200
    msg_rmv = requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': dm_message_data['message_id']})
    assert msg_rmv.status_code == 200

    # test user/stats: user_stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200

    # channels joined
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert len(response_data['user_stats']['channels_joined']) == 2
    # dms joined
    assert response_data['user_stats']['dms_joined'][1]['num_dms_joined'] == 1 
    assert len(response_data['user_stats']['dms_joined']) == 2
    # messages sent
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert len(response_data['user_stats']['messages_sent']) == 3
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][4]['num_messages_exist'] == 0
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 5
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 2 
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 2
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0
    
def test_user_stats_users_stats_channel_leave():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_1_data = channel_1.json()                              
    channel_2 = requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})

    channel_2_data = channel_2.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2_data['auth_user_id']})
    message_send1_response = requests.post(config.url + 'message/send/v1', json={'token': user2_data['token'],
                                                                           'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
    message_send1_data = message_send1_response.json()
    requests.post(config.url + 'message/send/v1', json={'token': user2_data['token'],
                                                                           'channel_id': channel_2_data['channel_id'], 'message': 'This is a second message'})
    requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user2_data['token'], 'message_id': message_send1_data['message_id']})

    channel_leave = requests.post(config.url + 'channel/leave/v1', json={
                             'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})

    assert channel_leave.status_code == 200

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user2_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert response_data['user_stats']['channels_joined'][2]['num_channels_joined'] == 2
    assert response_data['user_stats']['channels_joined'][3]['num_channels_joined'] == 1
    assert type(response_data['user_stats']['channels_joined'][2]['time_stamp']) == int
    assert len(response_data['user_stats']['channels_joined']) == 4
    # test dms joined
    assert response_data['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert type(response_data['user_stats']['dms_joined'][0]['time_stamp']) == int
    assert len(response_data['user_stats']['dms_joined']) == 1
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert len(response_data['user_stats']['messages_sent']) == 3
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2
    assert stats_response_data['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 1
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 4
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 1
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert stats_response_data['workspace_stats']['channels_exist'][2]['num_channels_exist'] == 2
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 3
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0

def test_involvement_rate_above_1():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_1_data = channel_1.json()                              
    channel_2 = requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})

    channel_2_data = channel_2.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2_data['auth_user_id']})
    message_send1_response = requests.post(config.url + 'message/send/v1', json={'token': user2_data['token'],
                                                                           'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})
    message_send1_data = message_send1_response.json()
    requests.post(config.url + 'message/send/v1', json={'token': user2_data['token'],
                                                                           'channel_id': channel_2_data['channel_id'], 'message': 'This is a second message'})
    requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user2_data['token'], 'message_id': message_send1_data['message_id']})

    channel_leave = requests.post(config.url + 'channel/leave/v1', json={
                             'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})

    assert channel_leave.status_code == 200

    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2_data['auth_user_id']})

    response = requests.get(config.url + 'user/stats/v1', params={'token': user2_data['token']})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert response_data['user_stats']['channels_joined'][2]['num_channels_joined'] == 2
    assert response_data['user_stats']['channels_joined'][3]['num_channels_joined'] == 1
    assert response_data['user_stats']['channels_joined'][4]['num_channels_joined'] == 2
    assert len(response_data['user_stats']['channels_joined']) == 5
    assert response_data['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert type(response_data['user_stats']['channels_joined'][2]['time_stamp']) == int
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert len(response_data['user_stats']['messages_sent']) == 3
    assert response_data['user_stats']['involvement_rate'] == 1.0

    

def test_user_stats_users_stats_dm_leave():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    assert dm_sent.status_code == 200

    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']}) 
    assert dm_leave.status_code == 200

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert len(response_data['user_stats']['channels_joined']) == 1
    # test dms joined
    assert response_data['user_stats']['dms_joined'][1]['num_dms_joined'] == 1
    assert response_data['user_stats']['dms_joined'][2]['num_dms_joined'] == 0
    assert len(response_data['user_stats']['dms_joined']) == 3

    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert len(response_data['user_stats']['messages_sent']) == 2
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 0.5

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 2
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 2
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 1
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 0.5


def test_user_stats_dm_remove():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    assert dm_sent.status_code == 200

    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']})
    assert dm_remove.status_code == 200 

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert len(response_data['user_stats']['channels_joined']) == 1
    # test dms joined
    assert response_data['user_stats']['dms_joined'][1]['num_dms_joined'] == 1
    assert response_data['user_stats']['dms_joined'][2]['num_dms_joined'] == 0
    assert len(response_data['user_stats']['dms_joined']) == 3
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert len(response_data['user_stats']['messages_sent']) == 2
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 0.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 0
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 3
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert stats_response_data['workspace_stats']['dms_exist'][2]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 3
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 1
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 0.0



def test_user_stats_second_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    message_data = dm_sent.json()    
    assert dm_sent.status_code == 200
    msg_rmv = requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})
    assert msg_rmv.status_code == 200

    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']}) 
    assert dm_leave.status_code == 200

    requests.delete(config.url + 'dm/remove/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']}) 

    stats_response = requests.get(config.url + 'user/stats/v1', params={'token': user2_data['token']})
    stats_response_data = stats_response.json()
    assert stats_response.status_code == 200
    assert stats_response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert stats_response_data['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert stats_response_data['user_stats']['dms_joined'][1]['num_dms_joined'] == 1 

def test_user_stats_return_types():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    stats_response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    assert stats_response.status_code == 200
    assert type(stats_response_data['user_stats']['involvement_rate']) == float
    assert type(stats_response_data['user_stats']['dms_joined'][0]['time_stamp']) == int
    assert type(stats_response_data['user_stats']['messages_sent'][0]['num_messages_sent']) == int
    assert type(stats_response_data['user_stats']['channels_joined'][0]['num_channels_joined']) == int

def test_user_stats_users_stats_channel_join():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})
    user2_data = user2.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_1_data = channel_1.json()                              
    requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})
    channel_1_join = requests.post(config.url + 'channel/join/v2',
                  json={'token': user2_data['token'], 'channel_id': channel_1_data['channel_id']})
    assert channel_1_join.status_code == 200
    
    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user2_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert response_data['user_stats']['channels_joined'][2]['num_channels_joined'] == 2
    assert type(response_data['user_stats']['channels_joined'][2]['time_stamp']) == int
    assert len(response_data['user_stats']['channels_joined']) == 3
    # test dms joined
    assert response_data['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert type(response_data['user_stats']['dms_joined'][0]['time_stamp']) == int
    assert len(response_data['user_stats']['dms_joined']) == 1
    # messages sent
    assert len(response_data['user_stats']['messages_sent']) == 1
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 1
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 1
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert stats_response_data['workspace_stats']['channels_exist'][2]['num_channels_exist'] == 2
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 3
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0

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

    remove_response = requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})
    assert remove_response.status_code == 200

    response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})

    response_data = response.json()

    assert response.status_code == 200
    assert response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 0



def test_users_stats_dm_leave():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    message_data = dm_sent.json()    
    assert dm_sent.status_code == 200
    msg_rmv = requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})
    assert msg_rmv.status_code == 200

    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a second message'})
    message_data = dm_sent.json()   
    dm_leave = requests.post(config.url + 'dm/leave/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']}) 
    assert dm_leave.status_code == 200

    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    assert stats_response.status_code == 200
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 1
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 4
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1 
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 2

def test_users_stats_dm_remove():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()
    dm_sent = requests.post(config.url + 'message/senddm/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id'], 
                                        'message': 'this is a message'})
    message_data = dm_sent.json()    
    assert dm_sent.status_code == 200
    msg_rmv = requests.delete(config.url + 'message/remove/v1', json={
                                       'token': user1_data['token'], 'message_id': message_data['message_id']})
    assert msg_rmv.status_code == 200

    dm_remove = requests.delete(config.url + 'dm/remove/v1', json = {'token': user1_data['token'] , 'dm_id': dm_data['dm_id']})
    assert dm_remove.status_code == 200 

    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    assert stats_response.status_code == 200
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 0
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 3
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1 
    assert stats_response_data['workspace_stats']['dms_exist'][2]['num_dms_exist'] == 0

def test_user_stats_users_stats_message_share():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    requests.post(config.url + 'auth/register/v2', json={'email': 'EMAIL@gmail.com',
                                                                 'password': 'password1', 'name_first': 'FIRST', 'name_last': 'LAST'})

    requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                                              'name': 'Second Channel', 'is_public': True})

    channel_data = channel_response.json()

    message_response = requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    
    message_data = message_response.json()
    requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel_data['channel_id'], 'message': "hello"})
    msg_share = requests.post(config.url + 'message/share/v1', json={
        'token': user1_data['token'], 'og_message_id': message_data['message_id'], 'message': "checkout this other message",
        'channel_id': channel_data['channel_id'], 'dm_id': -1})

    assert msg_share.status_code == 200

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert response_data['user_stats']['channels_joined'][2]['num_channels_joined'] == 2
    assert len(response_data['user_stats']['channels_joined']) == 3
    # test dms joined
    assert len(response_data['user_stats']['dms_joined']) == 1
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert response_data['user_stats']['messages_sent'][3]['num_messages_sent'] == 3
    assert len(response_data['user_stats']['messages_sent']) == 4
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2
    assert stats_response_data['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 3
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 4
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 1
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert stats_response_data['workspace_stats']['channels_exist'][2]['num_channels_exist'] == 2
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 3
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 0.5

def test_user_stats_users_stats_message_edit():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_data = channel_response.json()

    message_response = requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    message_data = message_response.json()
    requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel_data['channel_id'], 'message': "hello"})
    edit_response = requests.put(config.url + 'message/edit/v1', json={'token': user1_data['token'],
                                                                       'message_id': message_data['message_id'], 'message': ''})
    assert edit_response.status_code == 200

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert len(response_data['user_stats']['channels_joined']) == 2
    # test dms joined
    assert len(response_data['user_stats']['dms_joined']) == 1
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert len(response_data['user_stats']['messages_sent']) == 3
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2
    assert stats_response_data['workspace_stats']['messages_exist'][3]['num_messages_exist'] == 1
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 4
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 1
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 2
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0

def test_user_stats_users_stats_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    channel_response = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'],
                                                           'name': 'First Channel', 'is_public': True})
    channel_data = channel_response.json()

    requests.post(config.url + 'message/send/v1', json={'token': user1_data['token'],
                                                                           'channel_id': channel_data['channel_id'], 'message': 'This is a message'})
    requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel_data['channel_id'], 'message': "hello"})

    future_timestamp = time_now() + 30
    assert type(future_timestamp) == int

    sendlater = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user1_data['token'], 'channel_id': channel_data['channel_id'], 'message': 'hello', 'time_sent': future_timestamp})

    assert sendlater.status_code == 200  # Success

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert response_data['user_stats']['channels_joined'][1]['num_channels_joined'] == 1 
    assert len(response_data['user_stats']['channels_joined']) == 2
    # test dms joined
    assert len(response_data['user_stats']['dms_joined']) == 1
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert response_data['user_stats']['messages_sent'][1]['num_messages_sent'] == 1
    assert response_data['user_stats']['messages_sent'][2]['num_messages_sent'] == 2
    assert len(response_data['user_stats']['messages_sent']) == 3
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert stats_response_data['workspace_stats']['messages_exist'][1]['num_messages_exist'] == 1
    assert stats_response_data['workspace_stats']['messages_exist'][2]['num_messages_exist'] == 2
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 3
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 1
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert stats_response_data['workspace_stats']['channels_exist'][1]['num_channels_exist'] == 1 
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 2
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0

# message_sendlaterdm

def test_user_stats_users_stats_sendlaterdm():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'Alice', 'name_last': 'Yu'})

    user2_data = user2.json()
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1_data['token'] , 'u_ids': [user2_data['auth_user_id']]})  
    assert dm_response.status_code == 200
    dm_data = dm_response.json()

    future_timestamp = time_now() + 30
    assert type(future_timestamp) == int

    response = requests.post(config.url + 'message/sendlaterdm/v1', json={
                    'token': user1_data['token'], 'dm_id': dm_data['dm_id'], 'message': 'hello', 'time_sent': future_timestamp})

    # test user stats
    response = requests.get(config.url + 'user/stats/v1', params={'token': user1_data['token']})
    response_data = response.json()
    assert response.status_code == 200
    # test channels joined
    assert response_data['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    assert len(response_data['user_stats']['channels_joined']) == 1
    # test dms joined
    assert response_data['user_stats']['dms_joined'][1]['num_dms_joined'] == 1
    assert len(response_data['user_stats']['dms_joined']) == 2
    # messages sent
    assert response_data['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert len(response_data['user_stats']['messages_sent']) == 1
    # involvement rate
    assert response_data['user_stats']['involvement_rate'] == 1.0

    # tests users/stats: workspace stats
    stats_response = requests.get(config.url + 'users/stats/v1', params={'token': user1_data['token']})
    stats_response_data = stats_response.json()
    # messages exist
    assert stats_response_data['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert len(stats_response_data['workspace_stats']['messages_exist']) == 1
    # dms exist
    assert stats_response_data['workspace_stats']['dms_exist'][1]['num_dms_exist'] == 1
    assert len(stats_response_data['workspace_stats']['dms_exist']) == 2
    # channels exist
    assert stats_response_data['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert len(stats_response_data['workspace_stats']['channels_exist']) == 1
    # utilization rate
    assert stats_response_data['workspace_stats']['utilization_rate'] == 1.0

'''
    test for notifications
'''


def test_valid_notification_channel_invite(create_first_user, create_second_user):
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

def test_valid_notification_channel_message(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 on a channel, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'Second Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})
    user2_profile = requests.get(config.url + 'user/profile/v1', params={
                            'token': user2['token'], 'u_id': user2['auth_user_id']})

    user2_profile_response = user2_profile.json()
    user2_handle = user2_profile_response['user']['handle_str']

    requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': f'@{user2_handle} This is a message'})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()
    assert len(response_receiver_data['notifications']) == 2
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

def test_invalid_notification_channel_message(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 on a channel, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})
    user2_profile = requests.get(config.url + 'user/profile/v1', params={
                            'token': user2['token'], 'u_id': user2['auth_user_id']})

    user2_profile_response = user2_profile.json()
    user2_handle = user2_profile_response['user']['handle_str']

    requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': f'@{user2_handle}'})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()
    assert len(response_receiver_data['notifications']) == 2
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

def test_channel_message_invalid_tag(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 on a channel, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})
    user2_profile = requests.get(config.url + 'user/profile/v1', params={
                            'token': user2['token'], 'u_id': user2['auth_user_id']})

    user2_profile_response = user2_profile.json()
    user2_handle = user2_profile_response['user']['handle_str']

    requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': f'z@'})

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


def test_valid_notification_dm_invite(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 on a channel, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    
    requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})  

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


def test_valid_notification_dm_message(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 on a channel, expects a notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    user2_profile = requests.get(config.url + 'user/profile/v1', params={
                            'token': user2['token'], 'u_id': user2['auth_user_id']})
    
    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})  

    dm_data = dm_response.json()

    user2_profile_response = user2_profile.json()
    user2_handle = user2_profile_response['user']['handle_str']

    requests.post(config.url + 'message/senddm/v1', json = {'token': user1['token'] , 'dm_id': dm_data['dm_id'], 'message': f'hello@{user2_handle}@hello This is a message'})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()
    assert len(response_receiver_data['notifications']) == 2
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

def test_valid_notification_react(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 21 times, expects 20 notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})


    message_reponse = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})

    message = message_reponse.json()
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()
    assert len(response_receiver_data['notifications']) == 2
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

def test_invalid_notification_react_no_longer_in_channel(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 21 times, expects 20 notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})

    message_reponse = requests.post(config.url + 'message/send/v1', json={'token': user2['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': 'This is a message'})

    message = message_reponse.json()

    requests.post(config.url + 'channel/leave/v1', json={
                             'token': user2['token'], 'channel_id': channel_1_data['channel_id']})    
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})

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

def test_invalid_notification_react_no_longer_in_dm(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 21 times, expects 20 notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    dm_response = requests.post(config.url + 'dm/create/v1', json = {'token': user1['token'] , 'u_ids': [user2['auth_user_id']]})  

    dm_data = dm_response.json()

    message_reponse = requests.post(config.url + 'message/senddm/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id'], 'message': 'this is message 1'})

    message = message_reponse.json()

    requests.post(config.url + 'dm/leave/v1', json = {'token': user2['token'] , 'dm_id': dm_data['dm_id']})  
    
    requests.post(config.url + 'message/react/v1', json = {'token': user1['token'], 'message_id': message['message_id'], 'react_id': 1})

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


def test_valid_notification_only_20(create_first_user, create_second_user):
    '''
    Error raised:
        None
    ExplanationL
        User 1 messages user 2 21 times, expects 20 notification for user 2
    '''

    user1 = create_first_user
    user2 = create_second_user

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2['auth_user_id']})
    user2_profile = requests.get(config.url + 'user/profile/v1', params={
                            'token': user2['token'], 'u_id': user2['auth_user_id']})

    user2_profile_response = user2_profile.json()
    user2_handle = user2_profile_response['user']['handle_str']

    for _ in range(21):
            requests.post(config.url + 'message/send/v1', json={'token': user1['token'],
                                                        'channel_id': channel_1_data['channel_id'], 'message': f'@{user2_handle} This is a message'})

    response_receiver = requests.get(config.url + 'notifications/get/v1',
                                     params={'token': user2['token']})
    response_sender = requests.get(config.url + 'notifications/get/v1',
                                   params={'token': user1['token']})
    response_receiver_data = response_receiver.json()
    response_sender_data = response_sender.json()
    assert len(response_receiver_data['notifications']) == 20
    assert len(response_sender_data['notifications']) == 0
    assert response_receiver.status_code == 200
    assert response_sender.status_code == 200

