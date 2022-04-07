from src.token import check_valid_token
from src.global_helper import check_valid_user
from src.users_helpers import return_profile
from src.user_helper import return_notifications


def user_profile_v1(token, u_id):
    '''
        Returns a given user's profile 
    '''

    check_valid_token(token)

    check_valid_user(u_id)

    profile_info = return_profile(u_id)

    return {"user": profile_info}


def notifications_get_v1(token):
    user_id = check_valid_token(token)['u_id']

    user_notifications = return_notifications(user_id)
    print(user_notifications)
    return {'notifications': user_notifications}
