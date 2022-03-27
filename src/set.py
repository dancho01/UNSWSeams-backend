from src.token import check_valid_token
from src.data_store import data_store
from src.set_helper import check_name, check_email, check_handle, insert_name, insert_email, insert_handle


def set_name_v1(token, name_first, name_last):
    user_info = check_valid_token(token)

    check_name(name_first, name_last)

    # Inserts the name_first and name_last into the database
    insert_name(user_info['u_id'], name_first, name_last)

    return {}


def set_email_v1(token, email):
    user_info = check_valid_token(token)
    check_email(email)

    # Inserts the email into the database
    insert_email(user_info['u_id'], email)

    return {}


def set_handle_v1(token, handle):
    user_info = check_valid_token(token)

    check_handle(handle)

    # Inserts the handle into the database
    insert_handle(user_info['u_id'], handle)

    return {}
