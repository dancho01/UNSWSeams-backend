from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from datetime import timezone
from src.token import check_valid_token
import datetime

def user_profile_v1(token, u_id):
    store = data_store.get()
    
    check_valid_token(token)
    
    if check_user_registered(u_id, store) == False:
        raise InputError(description='one of the user ids does not refer to valid user')
    
    user_info = return_member_information(u_id, store)

    return user_info 