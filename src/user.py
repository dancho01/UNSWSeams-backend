from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from datetime import timezone
from src.token import check_valid_token
from src.global_helper import check_valid_user
import datetime

def user_profile_v1(token, u_id):
    store = data_store.get()
    
    check_valid_token(token)
    
    check_valid_user(u_id)
    
    user_info = return_member_information(u_id, store)

    return user_info 