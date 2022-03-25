import re
from src.data_store import data_store
from src.error import InputError
from src.token import hash, generate_token
from src.auth_helper import generate_new_handle, check_info
from src.token import hash, generate_token, check_valid_token
from src.global_helper import generate_user_id

AUTH_COUNTER = 0


def auth_login_v1(email, password):
    '''
    This function logs in a registered user, given their email and password
    Arguments:
        email         string         - the registered user's email
        password      string         - the registered user's password

    Exceptions:
        InputError      - Occurs when email entered does not belong to a user
        InputError      - Occurs when password is not correct

    Return Value:
        Returns a dictionary with the key 'auth_user_id', an integer value, if
        login is successful
    '''
    store = data_store.get()

    # iterates through users to check if email belongs to a user
    found = False
    for user in store['users']:
        if user['email'] == email:
            found = True

    # InputError is raised if valid email is not found
    if found != True:
        raise InputError(description="This email is not registered!")

    for user in store['users']:
        if user['email'] == email:
            # InputError is raised if password does not match
            if user['password'] != hash(password):
                raise InputError(description="Incorrect Password!")
            else:
                token = generate_token(user['auth_user_id'])
                return {'auth_user_id': user['auth_user_id'],
                        'token': token}


def auth_register_v1(email, password, name_first, name_last):
    '''
    This function registers a user, given the input of their first name, last name,
    email address and password, creating a new account for them. It is also responsible
    for generating the handle for the user. The handle must be unique for each user,
    so if a handle generated already exists, then a number is appended to it until
    it is unique.

    Arguments:
        email           string         - the user's email they want to register with
        password        string         - the user's intended password to use
        name_first      string         - the user's first name
        name_last       string         - the user's last name

    Exceptions:
        InputError      - Occurs when email entered is not a valid channel
        InputError      - Occurs when email address is already being used by another user
        InputError      - Occurs when length of password is less than 6 characters
        InputError      - Occurs when length of name_first is not between 1 and 50
                        characters inclusive
        InputError      - Occurs when length of name_last is not between 1 and 50 
                        characters inclusive

    Return Value:
        Returns a dictionary with the key 'auth_user_id', which is an integer value, if
        account is successfully created
    '''

    store = data_store.get()

    check_info(name_first, name_last, password, email)

    # creating handle from first and last name
    final_handle = generate_new_handle(name_first, name_last, store)

    # associating global permissions to user_id
    if len(store['users']) == 0:
        perms = 1
    else:
        perms = 2

    new_id = generate_user_id()

    # adding all information to dictionary
    new_user = {'auth_user_id': new_id, 'name_first': name_first, 'name_last': name_last,
                'email': email, 'password': hash(password), 'handle': final_handle, 'global_permissions': perms, 'active': True}

    store['users'].append(new_user)

    return {
        'auth_user_id': new_id,
        'token': generate_token(new_id),
    }


def auth_logout(token):
    store = data_store.get()
    user_info = check_valid_token(token)

    store['session_list'].remove(hash(user_info['session_id']))

    return {}
