from src.token import check_valid_token
from src.data_store import data_store
from src.set_helper import check_name, check_email, check_handle, insert_name, insert_email, insert_handle


def set_name_v1(token, name_first, name_last):
    '''
        checks if token is valid using check_valid_token,
        uses check_name to check for input errors and uses
        insert_name to insert the new name into the datastruct
    '''
    user_info = check_valid_token(token)

    check_name(name_first, name_last)

    # Inserts the name_first and name_last into the database
    insert_name(user_info['u_id'], name_first, name_last)

    return {}


def set_email_v1(token, email):
    '''
        checks if token is valid using check_valid_token,
        check_email checks if the email is in the right format
        and insert_email inserts the users new email into the 
        datastruct
    '''
    user_info = check_valid_token(token)

    check_email(email)

    # Inserts the email into the database
    insert_email(user_info['u_id'], email)

    return {}


def set_handle_v1(token, handle):
    '''
        checks if token is valid using check_valid_token,
        check_handle is used to check syntax of the new handle,
        insert_handle is used to insert the new handle into the
        datastruct
    '''
    user_info = check_valid_token(token)

    check_handle(handle)

    # Inserts the handle into the database
    insert_handle(user_info['u_id'], handle)

    return {}
