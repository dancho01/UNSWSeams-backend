from src.token import check_valid_token
from src.users_helpers import return_users_information


def users_all_v1(token):
    '''
    Returns a list of all users and their associated details.
    Args:
        token           str         user's token     
    Return Value:
        Returns dictionary containing {users} dictioanry, containing a list of dictionaries contains
        {auth_user_id, email, first name, last name, and handle}
    '''

    check_valid_token(token)

    users_info = return_users_information()

    return {'users': users_info}
