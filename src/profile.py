from src.token import check_valid_token
from src.data_store import data_store
from src.profile_helper import check_name, check_email, check_handle


def set_name_v1(token, name_first, name_last):
    user_info = check_valid_token(token)

    check_name(name_first, name_last)

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == user_info['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last

    data_store.set(store)

    return {}


def set_email_v1(token, email):
    user_info = check_valid_token(token)
    check_email(email)

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == user_info['u_id']:
            user['email'] = email

    data_store.set(store)

    return {}


def set_handle_v1(token, handle):
    user_info = check_valid_token(token)
    check_handle(handle)

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == user_info['u_id']:
            user['handle'] = handle

    return {}
