from re import U
from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from src.token import check_valid_token
from src.global_helper import check_valid_user
from src.users_helpers import return_profile


def user_profile_v1(token, u_id):
    '''
        Returns a given user's profile 
    '''

    check_valid_token(token)

    check_valid_user(u_id)

    profile_info = return_profile(u_id)

    return {"user": profile_info}
