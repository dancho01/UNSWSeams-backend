import pytest
import requests
import random
import string
from src import config


@pytest.fixture
def create_first_user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email123@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user1 = user1.json()
    return user1


@pytest.fixture
def create_second_user():
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'testemail@gmail.com',
                                                                 'password': 'elephant130', 'name_first': 'Daniel', 'name_last': 'Cho'})
    user2 = user2.json()
    return user2


@pytest.fixture
def generate_invalid_name():
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(60))
    return invalid_message


@pytest.fixture
def generate_invalid_handle():
    invalid_message = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(30))
    return invalid_message


@pytest.fixture
def create_public_channel_and_dm(create_first_user, create_second_user):

    user1, user2 = create_first_user, create_second_user

    ch1 = requests.post(config.url + 'channels/create/v2',
                        json={'token': user2['token'], 'name': 'ch1', 'is_public': True})

    channel1_data = ch1.json()

    requests.post(config.url + 'channel/addowner/v1', json={'token': user2['token'], 'channel_id': channel1_data['channel_id'],
                                                            'u_id': user2['auth_user_id']})

    response = requests.post(config.url + 'channel/join/v2', json={
                             'token': user1['token'], 'channel_id': channel1_data['channel_id']})

    requests.post(config.url + 'dm/create/v1',
                  json={'token': user1['token'], 'u_ids': [user2['auth_user_id']]})

    return user1


'''
set_name
'''


def test_name_first_too_long(create_first_user, generate_invalid_name):

    user = create_first_user

    response = requests.put(config.url + 'user/profile/setname/v1',
                            json={'token': user['token'], 'name_first': 'Jacob', 'name_last': generate_invalid_name})

    assert response.status_code == 400


def test_name_last_too_long(create_first_user, generate_invalid_name):
    user = create_first_user

    response = requests.put(config.url + 'user/profile/setname/v1',
                            json={'token': user['token'], 'name_first': generate_invalid_name, 'name_last': 'Jacks'})

    assert response.status_code == 400


def test_valid_names(create_first_user):
    user = create_first_user

    name_first, name_last = "jack", "bobs"

    response = requests.put(config.url + 'user/profile/setname/v1',
                            json={'token': user['token'], 'name_first': name_first, 'name_last': name_last})

    assert response.status_code == 200


def test_valid_names_in_channel_and_dm(create_public_channel_and_dm):
    user1 = create_public_channel_and_dm

    name_first, name_last = "jack", "bobs"

    response = requests.put(config.url + 'user/profile/setname/v1',
                            json={'token': user1['token'], 'name_first': name_first, 'name_last': name_last})

    assert response.status_code == 200


'''
set_email
'''


def test_invalid_email(create_first_user):
    user = create_first_user

    response = requests.put(config.url + 'user/profile/setemail/v1',
                            json={'token': user['token'], 'email': "gmail"})

    assert response.status_code == 400


def test_email_already_registered(create_first_user, create_second_user):
    user = create_first_user

    email = "testemail@gmail.com"

    response = requests.put(config.url + 'user/profile/setemail/v1',
                            json={'token': user['token'], 'email': email})

    assert response.status_code == 400


def test_valid_email(create_first_user):
    user = create_first_user

    email = "awdasadad@gmail.com"

    response = requests.put(config.url + 'user/profile/setemail/v1',
                            json={'token': user['token'], 'email': email})

    assert response.status_code == 200


def test_valid_email_in_channel_and_dm(create_public_channel_and_dm):
    user1 = create_public_channel_and_dm

    email = "awdasadad@gmail.com"

    response = requests.put(config.url + 'user/profile/setemail/v1',
                            json={'token': user1['token'], 'email': email})

    assert response.status_code == 200


'''
set_handle
'''


def test_handle_too_long(create_first_user, generate_invalid_handle):
    user = create_first_user

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user['token'], 'handle_str': generate_invalid_handle})

    assert response.status_code == 400


def test_handle_too_short(create_first_user):
    user = create_first_user

    handle = 'ab'

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user['token'], 'handle_str': handle})

    assert response.status_code == 400


def test_handle_not_alnum(create_first_user):
    user = create_first_user

    handle = 'ab!--_'

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user['token'], 'handle_str': handle})

    assert response.status_code == 400


def test_handle_exists(create_first_user, create_second_user):
    user1 = create_first_user

    user2_handle = "danielcho"

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user1['token'], 'handle_str': user2_handle})

    assert response.status_code == 400


def test_valid_handle(create_first_user):
    user1 = create_first_user

    user2_handle = "validHandle"

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user1['token'], 'handle_str': user2_handle})

    assert response.status_code == 200


def test_valid_handle_in_channel_and_dm(create_public_channel_and_dm):
    user1 = create_public_channel_and_dm

    handle = "validHandle"

    response = requests.put(config.url + 'user/profile/sethandle/v1',
                            json={'token': user1['token'], 'handle_str': handle})

    assert response.status_code == 200
