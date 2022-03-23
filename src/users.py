from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from datetime import timezone
from src.token import check_valid_token
from src.users_helpers import return_users_information
import datetime


def users_all_v1(token):
    store = data_store.get()
       
    check_valid_token(token)
        
    users_info = return_users_information(store)

    return {'users': users_info}
