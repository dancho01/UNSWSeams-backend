import pytest
import requests
import json
from src import config

''' tests for auth/register/v2  '''

def test_invalid_first_name():
    '''
    Error raised:
        InputError: length of name_first is not between 1 and 50 characters inclusive
    Explanation:
        The string inputted is an empty string, less than 1 character   
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': '', 'name_last': 'Last'})
    assert response.status_code == 400


def test_invalid_last_name():
    '''
    Error raised:
        InputError: length of name_last is not between 1 and 50 characters inclusive
    Explanation:
        The string inputted is an empty string, less than 1 character
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': 'First', 'name_last': ''})
    assert response.status_code == 400


def test_invalid_email_format():
    '''
    Error raised:
        InputError: the email entered is not in a valid format 
    Explanation:
        The email entered is missing '@' and a '.'
        
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'emailgmailcom',
                                                                    'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    assert response.status_code == 400


def test_invalid_password():
    '''
    Error raised:
        InputError: length of password is less than 6 characters
    Explanation:
        the password entered in is 5 characters, which is less than 6
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'short', 'name_first': 'First', 'name_last': 'Last'})
    assert response.status_code == 400


def test_duplicate_emails():
    '''
    Error raised:
        InputError: email address is already being used by another user
    Explanation:
        the email entered has already been used to register another user    
    '''
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'anotherpassword', 'name_first': 'Anotherfirst', 'name_last': 'Anotherlast'})
    assert user2.status_code == 400


def test_long_name():
    '''
    Error raised:
        None
    Explanation:
        Succesfully registers a user with the given valid names 
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': 'uvuvwevwevwe', 'name_last': 'onyetenyevwe'})
    assert response.status_code == 200


def test_not_alnum_name():
    '''
    Error raised:
        None
    Explanation:
        succesfully registers a user with the given name that are not all alpha numeric        
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': 'uvuvwevwevwe!!!', 'name_last': 'onyetenyevwe'})
    assert response.status_code == 200


def test_register_success():
    '''
    Error raised:
        None
    Explanation:
        succesfully registers a user with no errors thrown 
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                    'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    assert response.status_code == 200


''' tests for auth/login/v2  '''


def test_email_no_user():
    '''
    Errors raised:
        InputError: email entered does not belong to a user
    Explanation:
        When the email entered has not been registed with yet   
    '''
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'invalidemail@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 400


def test_password_incorrect():
    '''
    Error raised:
        InputError: password is not correct
    Explanation:
        The password does not match with the password entered for the corresponding email   
    '''
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'wrongpassword'})
    assert login_response.status_code == 400


def test_login_no_user_registered():
    '''
    Error raised:
        InputError: email entered does not belong to a user
    Explanation:
        No user has registered yet so login is unsuccessful
    '''
    requests.delete(config.url + 'clear/v1')
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 400


def test_login_success():
    '''
    Error raised: 
        None
    Explanation:
        Login is succesful as email and password are all valid and corresponds 
    '''
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                         'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    login_response = requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'password'})
    assert login_response.status_code == 200


def test_logout():
    '''
    Error raised:
        None
    Explanation:
        Logout is succesful with the given token of a user registered  
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                              'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    register_response = r1.json()
    logout_response = requests.post(
        config.url + 'auth/logout/v1', json={'token': register_response['token']})

    assert logout_response.status_code == 200


def test_logout_return():
    '''
    Error raised:
        None
    Explanation:
        Tests that the return type of logout is an empty dictionary   
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                              'password': 'password', 'name_first': 'First', 'name_last': 'Last'})
    register_response = r1.json()
    logout_response = requests.post(
        config.url + 'auth/logout/v1', json={'token': register_response['token']})

    logout_return = logout_response.json()

    assert logout_return == {}

def test_invalid_session_id():
    '''
        check user's handle is reusable - i.e. register someone else with the exact same name and that handle should be the same as
        previous user's handle
    '''
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First2', 'name_last': 'Last'})
    requests.post(config.url + 'auth/login/v2', json={'email': 'email@gmail.com',
                                                                       'password': 'password'})
    response = requests.post(config.url + 'auth/logout/v1', json={'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxLCJzZXNzaW9uX2lkIjoiZGQ1NWFkMzcxZjRjNmQyNTExYWFlYjNkMzkwMmNiZGJhZWFmZGFiNDdiMWQzOTI2NDUzYTFhNTg5MjQzZTZjMCJ9.dwiWCf54xraWhX4wuPogufTYEKgraxuRR392DNXPvmk'})
    assert response.status_code == 403 # AccessError
