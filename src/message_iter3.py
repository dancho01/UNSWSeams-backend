from src.data_store import data_store
from src.error import InputError, AccessError
from src.token import check_valid_token
from src.channel_helper import check_message
from src.iter3_message_helper import is_user_joined, return_messages_with_query
import re

def search_v1(token, query_str):
    store = data_store.get()
    user_id = check_valid_token(token)['u_id']

    check_message(query_str)
    
    query_collection = []
    
    for channel in store['channels']:
        if is_user_joined(channel, user_id): 
            query_collection = return_messages_with_query(query_str, channel, query_collection)        
    
    for dm in store['dms']:
        if is_user_joined(dm, user_id):
            query_collection = return_messages_with_query(query_str, dm, query_collection)                
    
    return {
        'messages': query_collection
    }
    
