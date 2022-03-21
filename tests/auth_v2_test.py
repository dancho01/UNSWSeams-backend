import pytest
import requests
import json
from src import config

''' tests for auth/register/v2  '''


def test_invalid_first_name():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': '', 'name_last': 'Last'})
    assert response.status_code == 400


def test_invalid_last_name():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': 'First', 'name_last': ''})
    assert response.status_code == 400


def test_invalid_email_format():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'emailgmailcom',
                                                                    'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    assert response.status_code == 400


def test_invalid_password():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'short', 'name_first': 'First', 'name_last': 'Last'})
    assert response.status_code == 400


def test_duplicate_emails():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'anotherpassword', 'name_first': 'Anotherfirst', 'name_last': 'Anotherlast'})
    assert user2.status_code == 400


def test_register_success():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={
        "email": "email@gmail.com",
        "password": "password",
        "name_first": "First",
        "name_last": "Last"
    })
    assert response.status_code == 200


''' tests for auth/login/v2  '''


def test_email_no_user():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'invalidemail@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 400


def test_password_incorrect():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'wrongpassword'})
    assert login_response.status_code == 400


def test_login_no_user_registered():
    requests.delete(config.url + 'clear/v1')
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 400


def test_login_success():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 200

    #register_data = register_response.json()
   # login_data = login_response.json()
