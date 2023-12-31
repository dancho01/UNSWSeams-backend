from src.token import check_valid_token
from src.users_helpers import return_users_information


def users_all_v1(token):
    '''
    Returns a list of all users and their associated details.
    '''

    check_valid_token(token)

    users_info = return_users_information()

    return {'users': users_info}
