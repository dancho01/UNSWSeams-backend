import re
from src.data_store import data_store
from src.error import InputError
from src.token import hash, generate_token
from src.auth_helper import generate_new_handle, check_info_syntax, \
    check_login, assign_permissions, \
    check_email_exist, generate_reset_code, \
    email_reset_code
from src.token import hash, generate_token, check_valid_token
from src.global_helper import generate_user_id
from src.channel_helper import time_now
from src import config
import urllib.request
from PIL import Image
import os


def auth_login_v1(email, password):
    '''
        Checks login information to first see if the email exists
        and if the password matches.

        If first layer of authentication is passed, a token is generated
        for the user.
    '''

    user_info = check_login(email, password)

    token = generate_token(user_info['u_id'], user_info['handle'])
    return {'auth_user_id': user_info['u_id'],
            'token': token}


def auth_register_v1(email, password, name_first, name_last):
    '''
        Checks input errors with check_info_syntax, a new
        handle is generated along with a new_id. After
        those are created, the information will be appended
        to store['users'] and the token and id will then be
        returned
    '''

    store = data_store.get()

    check_info_syntax(name_first, name_last, password, email)

    # creating handle from first and last name
    final_handle = generate_new_handle(name_first, name_last, store)

    new_id = generate_user_id()

    # adding all information to dictionary

    img_url = 'https://upload.wikimedia.org/wikipedia/commons/c/c9/Cat.jpeg'

    store['users'].append({'auth_user_id': new_id,
                           'name_first': name_first,
                           'name_last': name_last,
                           'email': email,
                           'password': hash(password),
                           'handle': final_handle,
                           'global_permissions': assign_permissions(),
                           'active': True,
                           'notifications': [],

                           'stats': {
                               'user_stats': {
                                   "channels_joined": [
                                       {
                                           "num_channels_joined": 0,
                                           "time_stamp": time_now()
                                       }
                                   ],
                                   "dms_joined": [
                                       {
                                           "num_dms_joined": 0,
                                           "time_stamp": time_now()
                                       }
                                   ],
                                   "messages_sent": [
                                       {
                                           "num_messages_sent": 0,
                                           "time_stamp": time_now()
                                       }
                                   ],
                                   "involvement_rate": 0.0
                               },
                               "total_channels_joined": 0,
                               "total_dms_joined": 0,
                               "total_messages_sent": 0
                           },
                           'profile_img_url': img_url})

    return {
        'auth_user_id': new_id,
        'token': generate_token(new_id, final_handle),
    }


def auth_logout(token):
    '''
        Checks the user for valid token, then removes them
        from the session_id list
    '''
    store = data_store.get()
    user_info = check_valid_token(token)

    store['session_list'].remove(user_info['session_id'])

    return {}


def auth_password_request(mail, email):
    '''
    Takes in an email, runs through some validation checks and
    sends an email to user with the reset code
    
    Args:
        mail        object
        email       str
        
    Return:
        returns nothing
    '''
    

    uid = check_email_exist(email)

    if uid == "":
        return {}

    code = generate_reset_code(uid)

    email_reset_code(email, code, mail)

    return {}


def auth_password_reset(code, new_pass):
    '''
    Given a reset code for a user, set that user's new password to the password 
    provided. Once a reset code has been used, it is then invalidated. 
    
    Args:
        code        str
        new_pass    str
        
    Return:
        returns nothing
    '''

    store = data_store.get()

    if not len(new_pass) >= 6:  # checking if password is valid
        raise InputError(description="Invalid Password")

    # iterating through a list of dicts. these dicts contain the reset code and the user_id the code belongs to
    for codes in store['reset_codes']:
        for user in store['users']:
            # finds the user who the reset code belongs to
            if user['auth_user_id'] == codes['uid']:
                if codes['code'] == int(code):  # checks if user inputted code is valid
                    # sets this users password
                    user['password'] = hash(new_pass)
                    del codes  # removes the reset_code and uid dict from reset_codes list
                    return
    raise InputError(description="Invalid Reset Code")
