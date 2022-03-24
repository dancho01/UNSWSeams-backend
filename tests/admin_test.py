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
