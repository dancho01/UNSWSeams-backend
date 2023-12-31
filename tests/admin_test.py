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
        tests when u_id does not refer to a valid user
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()

    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                                          'u_id': user1_data['auth_user_id'] + 1})
    assert response.status_code == 400  # inputError


def test_admin_user_remove_only_global_owner_left():
    """
        tests when u_id refers to a user who is the only global owner
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
    requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
                                                                       'permission_id': GLOBAL_OWNER})
    response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user3_data['token'],
                                                                          'u_id': user1_data['auth_user_id']})
    assert response.status_code == 403  # AccessError


def test_call_user_profile_after_removing_user():
    """
        ensure profile is still retrievable with user/profile after removing the user
    """
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


def test_check_removed_from_all_channels():
    """
    check user is removed from all channels
    """
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

    response = requests.get(config.url + 'channel/details/v2', params={'token': user1_data['token'],
                                                                       'channel_id': channel_1_data['channel_id']})
    response_data = response.json()

    assert len(response_data['all_members']) == 1

    response = requests.get(config.url + 'channel/details/v2', params={'token': user1_data['token'],
                                                                       'channel_id': channel_2_data['channel_id']})
    response_data = response.json()

    assert len(response_data['all_members']) == 1


def test_check_removed_from_all_dms():
    """
    check user is removed from all dms
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email1@gmail.com',
                                                                 'password': 'password', 'name_first': 'First1', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    user2_data = user2.json()
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'email3@gmail.com',
                                                                 'password': 'password', 'name_first': 'First3', 'name_last': 'Last'})
    user3_data = user3.json()

    dm_1 = requests.post(config.url + 'dm/create/v1',
                         json={'token': user1_data['token'], 'u_ids': [user2_data['auth_user_id']]})
    dm_1_data = dm_1.json()
    assert dm_1.status_code == 200
    dm_2 = requests.post(config.url + 'dm/create/v1',
                         json={'token': user1_data['token'], 'u_ids': [user3_data['auth_user_id']]})
    dm_2_data = dm_2.json()
    assert dm_2.status_code == 200
    dm_3 = requests.post(config.url + 'dm/create/v1',
                         json={'token': user2_data['token'], 'u_ids': [user3_data['auth_user_id']]})
    dm_3_data = dm_3.json()
    assert dm_3.status_code == 200

    dm_4 = requests.post(config.url + 'dm/create/v1',
                         json={'token': user2_data['token'], 'u_ids': [user1_data['auth_user_id']]})
    dm_4_data = dm_4.json()
    assert dm_4.status_code == 200

    dm_5 = requests.post(config.url + 'dm/create/v1', json={'token': user2_data['token'], 'u_ids': [user1_data['auth_user_id'],
                                                                                                    user3_data['auth_user_id']]})
    dm_5_data = dm_5.json()
    assert dm_5.status_code == 200

    dm_6 = requests.post(config.url + 'dm/create/v1', json={'token': user1_data['token'], 'u_ids': [user2_data['auth_user_id'],
                                                                                                    user3_data['auth_user_id']]})
    dm_6_data = dm_6.json()
    assert dm_6.status_code == 200

    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                               'u_id': user2_data['auth_user_id']})

    dm_details_1 = requests.get(config.url + 'dm/details/v1',
                                params={'token': user1_data['token'], 'dm_id': dm_1_data['dm_id']})
    assert dm_details_1.status_code == 200
    dm_details_1_data = dm_details_1.json()
    assert len(dm_details_1_data['members']) == 1

    response2 = requests.get(config.url + 'dm/details/v1', params={'token': user1_data['token'],
                                                                   'dm_id': dm_2_data['dm_id']})
    response2_data = response2.json()

    assert len(response2_data['members']) == 2

    dm_details_3 = requests.get(config.url + 'dm/details/v1',
                                params={'token': user3_data['token'], 'dm_id': dm_3_data['dm_id']})
    assert dm_details_3.status_code == 200
    dm_details_3_data = dm_details_3.json()
    assert len(dm_details_3_data['members']) == 1

    dm_details_4 = requests.get(config.url + 'dm/details/v1',
                                params={'token': user1_data['token'], 'dm_id': dm_4_data['dm_id']})
    assert dm_details_4.status_code == 200
    dm_details_4_data = dm_details_4.json()
    assert len(dm_details_4_data['members']) == 1

    dm_details_5 = requests.get(config.url + 'dm/details/v1',
                                params={'token': user1_data['token'], 'dm_id': dm_5_data['dm_id']})
    assert dm_details_5.status_code == 200
    dm_details_5_data = dm_details_5.json()
    assert len(dm_details_5_data['members']) == 2

    dm_details_6 = requests.get(config.url + 'dm/details/v1',
                                params={'token': user1_data['token'], 'dm_id': dm_6_data['dm_id']})
    assert dm_details_6.status_code == 200
    dm_details_6_data = dm_details_6.json()
    assert len(dm_details_6_data['members']) == 2


def test_check_not_in_users_all():
    """
    ensure the removed user is not in users/all/v1 after being removed.
    check not inlcuded in users returned by users/all.
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                               'u_id': user2_data['auth_user_id']})
    response = requests.get(config.url + 'users/all/v1',
                            params={'token': user1_data['token']})
    response_data = response.json()
    assert len(response_data['users']) == 1


def test_removing_Seams_OG_owner_while_multiple_global_owners():
    """
        Test that a Seams owner removing another Seams owner(including original owner) works.
        Test removing OG owner.
    """

    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
                                                                       'permission_id': 1})
    requests.delete(config.url + 'admin/user/remove/v1',
                    json={'token': user2_data['token'], 'u_id': user1_data['auth_user_id']})
    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user2_data['token'], 'u_id': user1_data['auth_user_id']})

    # check first name and last name is "Removed" "user"
    profile_response_data = profile_response.json()
    assert profile_response_data['user']['name_first'] == 'Removed'
    assert profile_response_data['user']['name_last'] == 'user'


def test_remove_other_Seams_owner():
    """
        test that removing the other Seams owner works
    """
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
    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    # check first name and last name is "Removed" "user"
    profile_response_data = profile_response.json()
    assert profile_response_data['user']['name_first'] == 'Removed'
    assert profile_response_data['user']['name_last'] == 'user'


def test_check_channel_message_contents_is_Removed_user():
    """
        Check that the removed user's messages in all channels are changed to "Removed user". 
        Check message contents is "Removed user". 
    """

    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    channel_1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_data['token'], 'name': 'First Channel',
                                                                       'is_public': True})
    channel_1_data = channel_1.json()
    requests.post(config.url + 'channel/invite/v2', json={'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'],
                                                          'u_id': user2_data['auth_user_id']})
    message = "hello"
    requests.post(config.url + 'message/send/v1', json={
        'token': user2_data['token'], 'channel_id': channel_1_data['channel_id'], 'message': message})
    requests.post(config.url + 'message/send/v1', json={
        'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'], 'message': message})
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user2_data['token'], 'channel_id': channel_1_data['channel_id'], 'message': "message 2"})
    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                               'u_id': user2_data['auth_user_id']})
    message_response = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1_data['token'], 'channel_id': channel_1_data['channel_id'], 'start': 0})
    message_response_data = message_response.json()
    assert message_response_data['messages'][1]['message'] == "Removed user"


def test_check_dm_message_contents_is_Removed_user():
    '''
        check that the removed user's messages in all dms are changed to "Removed user"
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email1@gmail.com',
                                                                 'password': 'password', 'name_first': 'First1', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    user2_data = user2.json()

    dm_1 = requests.post(config.url + 'dm/create/v1',
                         json={'token': user1_data['token'], 'u_ids': [user2_data['auth_user_id']]})
    dm_1_data = dm_1.json()
    assert dm_1.status_code == 200

    message = "hello"
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user2_data['token'], 'dm_id': dm_1_data['dm_id'], 'message': message})
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_data['token'], 'dm_id': dm_1_data['dm_id'], 'message': message})
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user2_data['token'], 'dm_id': dm_1_data['dm_id'], 'message': "message 2"})

    requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                               'u_id': user2_data['auth_user_id']})
    message_response = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1_data['token'], 'dm_id': dm_1_data['dm_id'], 'start': 0})
    message_response_data = message_response.json()
    assert message_response_data['messages'][0]['message'] == "Removed user"


def test_email_is_reregisterable_after_user_remove():
    '''
        check user's email is re-registerable after the user is removed
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email1@gmail.com',
                                                                 'password': 'password', 'name_first': 'First1', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    user2_data = user2.json()
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                                                 'u_id': user2_data['auth_user_id']})
    assert remove_response.status_code == 200
    rego_response = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                         'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    assert rego_response.status_code == 200


def test_handle_is_reusable_after_user_removal():
    '''
        check user's handle is reusable - i.e. register someone else with the exact same name and that handle should be the same as
        previous user's handle
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email1@gmail.com',
                                                                 'password': 'password', 'name_first': 'First1', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    user2_data = user2.json()
    profile_response_1 = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    assert profile_response_1.status_code == 200
    profile_response_1_data = profile_response_1.json()
    original_handle = profile_response_1_data['user']['handle_str']

    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user1_data['token'],
                                                                                 'u_id': user2_data['auth_user_id']})
    assert remove_response.status_code == 200

    profile_response = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_data['auth_user_id']})
    assert profile_response.status_code == 200
    profile_response_data = profile_response.json()
    # check removed user's handle does not get deleted from OG user profile
    assert profile_response_data['user']['handle_str'] == original_handle

    user2_again = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                       'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    user2_again_data = user2_again.json()
    profile_response_2 = requests.get(config.url + 'user/profile/v1', params={
        'token': user1_data['token'], 'u_id': user2_again_data['auth_user_id']})
    assert profile_response_2.status_code == 200
    profile_response_2_data = profile_response_2.json()
    assert profile_response_2_data['user']['handle_str'] == original_handle


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
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
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


def test_change_user_permission_test_owner_permissions():
    """
        test that the user permissions are able to be changed to global owner, by a global owner
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1_data = user1.json()
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email2@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2_data = user2.json()
    response1 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
                                                                                   'permission_id': 1})
    assert response1.status_code == 200

    response2 = requests.delete(config.url + 'admin/user/remove/v1', json={'token': user2_data['token'],
                                                                           'u_id': user1_data['auth_user_id']})
    assert response2.status_code == 200


def test_user_permission_change_owner_to_member():
    """
        test that user permissions are able to be changed back to normal member, by another global owner
    """
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
    response1 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user1_data['token'], 'u_id': user2_data['auth_user_id'],
                                                                                   'permission_id': 1})
    assert response1.status_code == 200

    response2 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user2_data['token'], 'u_id': user3_data['auth_user_id'],
                                                                                   'permission_id': 1})
    assert response2.status_code == 200

    response3 = requests.post(config.url + 'admin/userpermission/change/v1', json={'token': user2_data['token'], 'u_id': user3_data['auth_user_id'],
                                                                                   'permission_id': 2})
    assert response3.status_code == 200
    assert json.loads(response3.text) == {}
