from ast import Global
import pytest
import requests
import json
from src import config
from src.data_store import data_store

GLOBAL_OWNER = 1
MEMBER_ONLY_GLOBAL_PERMISSIONS = 2

def test_admin_user_remove_u_id_not_valid():
    """
    u_id does not refer to a valid user
    """
    requests.delete(config.url + 'clear/v1')
    print(data_store.get())
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    print(data_store.get())
    print(user1_data)
    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user1_data['auth_user_id'] + 1})
    print(data_store.get())
    assert response.status_code == 400  # inputError

def test_admin_user_remove_only_global_owner_left():
    """
        u_id refers to a user who is the only global owner
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()

    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user1_data['auth_user_id']})
    assert response.status_code == 400  # inputError

def test_admin_user_remove_auth_user_not_global_owner():
    '''
        the authorised user is not a global owner
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'email3@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user3_data = user3.json()
    print(data_store.get())
    requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
        'permission_id': GLOBAL_OWNER})
    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user3_data['token'],
        'u_id': user1_data['auth_user_id']})
    assert response.status_code == 403  # AccessError

# can you call user/profile after removing user
# ensure profile is still retrievable
def test_call_user_profile_after_removing_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    assert profile_response.status_code == 200


    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user2_data['auth_user_id']})
    assert response.status_code == 200
    profile_response_2 = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    assert profile_response_2.status_code == 200

    # check first name and last name is "Removed" "user"
    profile_response_2_data = profile_response_2.json()
    assert profile_response_2_data['user']['name_first'] == 'Removed'
    assert profile_response_2_data['user']['name_last'] == 'user'

def test_check_removed_from_all_channels_dms():
    """
need to put in working channels/list function
    """
# check removed from all channels/dms
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'email3@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user3_data = user3.json()

    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()

    channel_2 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'Second Channel',
                                                                       'is_public': False})
    channel_2_data = channel_2.json()

    channel_3 = requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'], 'name': 'Third Channel',
                                                                       'is_public': False})
    channel_3_data = channel_3.json()

    channel_4 = requests.post(config.url + 'channels/create/v2', json={'token': user2_data['token'], 'name': 'Fourth Channel',
                                                                       'is_public': True})
    channel_4_data = channel_4.json()

    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})

    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_2_data['channel_id'],
                                                                     'u_id': user2_data['auth_user_id']})
                                                                
    requests.post(config.url + 'channel/invite/v2', json={'token': user2_data['token'], 'channel_id': channel_3_data['channel_id'],
                                                                     'u_id': user3_data['auth_user_id']})

    requests.post(config.url + 'channel/invite/v2', json={'token': user2_data['token'], 'channel_id': channel_4_data['channel_id'],
                                                                     'u_id': user3_data['auth_user_id']})            

    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user2_data['auth_user_id']})                                                                                    

    response = requests.get(config.url + 'channels/list/v2',
                            params={'token': user2_data['token']})
    
    response_data = response.json()
    #assert response_data['channels'][0] == {}
    #assert response_data['channels'][1] == {}
    #assert response_data['channels'][2] == {}
    #assert response_data['channels'][3] == {}

def test_check_not_in_users_all():
    """
    need to put in working users/all function
    """
# chceck not inlcuded in users returned by users/all
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user2_data['auth_user_id']})   
    response = requests.get(config.url + 'users/all/v1', params = {'token' : user1_data['token']})
    response_data = response.json()
    #assert len(response_data['users']) == 1

    
def test_removing_Seams_OG_owner_while_multiple_global_owners():
# Seams owner removing another Seams owner(including original owner)
    # test remove OG owner
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
        'permission_id': 1})
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user2_data['token'],
        'u_id': user1_data['auth_user_id']})   
    #response = requests.get(config.url + 'users/all/v1', params = {'token' : user1_data['token']})
    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user2_data['token'], 'u_id': user1_data['auth_user_id']})
    # check first name and last name is "Removed" "user"
    profile_response_data = profile_response.json()
    assert profile_response_data['user']['name_first'] == 'Removed'
    assert profile_response_data['user']['name_last'] == 'user'

def test_remove_other_Seams_owner():
    # test remove other Seams owner
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
        'permission_id': 1})
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
        'u_id': user2_data['auth_user_id']})   
    #response = requests.get(config.url + 'users/all/v1', params = {'token' : user1_data['token']})
    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    # check first name and last name is "Removed" "user"
    profile_response_data = profile_response.json()
    assert profile_response_data['user']['name_first'] == 'Removed'
    assert profile_response_data['user']['name_last'] == 'user'


# check message contents is "Removed user"

# check first name and last name is "Removed" "user"

# check user's email is registerable 


# check user's handle is reusable - i.e. register someone else with the exact same name and that handle should be the same as
# previous user's handle




"""
    admin/userpermission/change/v1 tests

"""
def test_admin_userpermission_change_u_id_invalid():
    """
    u_id does not refer to a valid user
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()

    response = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user1_data['auth_user_id'] + 1,
        'permission_id': GLOBAL_OWNER})
    assert response.status_code == 400  # inputError

def test_admin_userpermission_change_u_id_is_sole_global_owner():
    """
    u_id refers to a user who is the only global owner and they are being demoted to a user
    - basically means demoting themselves since ONLY global owners can change users' permissions
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()

    response = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user1_data['auth_user_id'],
        'permission_id': MEMBER_ONLY_GLOBAL_PERMISSIONS})
    assert response.status_code == 400  # inputError

def test_admin_userpermission_change_u_id_permission_id_invalid():
    """
    permission_id is invalid
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
        'permission_id': 3})
    assert response.status_code == 400  # inputError

def test_admin_userpermission_change_u_id_permissions_already_given():
    """
    the user already has the permissions level of permission_id
    """
    #global GLOBAL_OWNER
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    # response1 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'],
    #     'u_id': user2_data['auth_user_id'], 'permission_id': 1})
    # assert response1.status_code == 200     # success
    response2 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'],
        'u_id': user2_data['auth_user_id'], 'permission_id': 2})
    assert response2.status_code == 400  # inputError

def test_admin_userpermission_change_auth_user_not_global_owner():
    """
    the authorised user is not a global owner
    """
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'email3@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user3_data = user3.json()
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user2_data['token'],
        'u_id': user3_data['auth_user_id'], 'permission_id': 1})
    assert response.status_code == 403  # AccessError


# # test a successful case
