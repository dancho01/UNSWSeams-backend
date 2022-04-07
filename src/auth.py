import re
from src.data_store import data_store
from src.error import InputError
from src.token import hash, generate_token
from src.auth_helper import generate_new_handle, check_info_syntax, check_login, assign_permissions
from src.token import hash, generate_token, check_valid_token
from src.global_helper import generate_user_id


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

    store['users'].append({'auth_user_id': new_id,
                           'name_first': name_first,
                           'name_last': name_last,
                           'email': email,
                           'password': hash(password),
                           'handle': final_handle,
                           'global_permissions': assign_permissions(),
                           'active': True,
                           'notifications': []})

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
