from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from src.auth_helper import decode_jwt, check_valid_token
from src.dm_helpers import check_for_duplicates_uids, return_handle, check_valid_dm, check_user_member_dm, return_dm_messages, generate_new_dm_id
from src.message_helper import generate_new_message_id
from datetime import timezone
import datetime


# DM Functions/Implementation details
def dm_create_v1(token, u_ids):
 
    store = data_store.get()
    
    # checks whether the token is valid and verifies user
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
     
    # if user is verified, the id of authorised user is stored      
    auth_user_id = check_valid_token(store, jwt_data)[1]
        
    for u_id in u_ids:
        if check_user_registered(u_id, store) == False:
            raise InputError(description='one of the user ids does not refer to valid user')
            
    if check_for_duplicates_uids(u_ids) == True:
        raise InputError(description='duplicate user ids not allowed')
    
    new_dm_id = generate_new_dm_id()
    
    list_handles = []
    for u_id in u_ids:
        list_handles.append(return_handle(u_id, store))
        
    list_handles.append(return_handle(auth_user_id, store))
        
    ordered_handles = sorted(list_handles)
    name = ', '.join(ordered_handles)
       
    new_dm = {'dm_id': new_dm_id,
              'name': name,
              'all_members': [],
              'messages': [],  
    }
    
    # adding owner to all_members list
    new_dm['all_members'].append(return_member_information(auth_user_id, store))
    
    # adding the rest of users to all_members list
    for u_id in u_ids:  
        new_dm['all_members'].append(return_member_information(u_id, store))    
        
    # only original creator of DM is added to owner
    new_dm['owner'] = return_member_information(auth_user_id, store)
    print(new_dm_id)
    
    store['dms'].append(new_dm)   
    data_store.set(store)
    
    return {
        'dm_id': new_dm_id,
    }



def dm_list_v1(token):
    store = data_store.get()
        
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]
     
    list_dms = []
    for dm in store['dms']:
        for member in dm['all_members']:
            if auth_user_id == member['u_id']:
                list_dms.append({'dm_id': dm['dm_id'], 'name': dm['name']})   
    
    return {
        'dms': list_dms
    }
    
    
def dm_remove_v1(token, dm_id):
   
    store = data_store.get()
    
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]
    
    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')
    
    dm_index = check_valid_dm(dm_id, store)[1]    
    
    auth_user_member = return_member_information(auth_user_id, store)
    
    if auth_user_member not in store['dms'][dm_index]['all_members']:
        raise AccessError(description='user is no longer in the DM')
    
    if store['dms'][dm_index]['owner']['u_id'] != auth_user_id:
        raise AccessError(description='authorised user is not the DM creator')
    
    
    store['dms'] = list(filter(lambda i: i['dm_id'] != dm_id, store['dms'])) 
    
    data_store.set(store)
    
    return {}
    
    
# always raises input error, need to fix
def dm_details_v1(token, dm_id):
    store = data_store.get()

    # checks if token is valid, verifying user
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]
    
    
    is_dm_valid = check_valid_dm(dm_id, store)
    if is_dm_valid == False:
        raise InputError(description='dm_id does not refer to a valid DM')    
   
    dm_index = is_dm_valid[1]
       
    dm_index = check_valid_dm(dm_id, store)[1]  
         
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')
            
    dm_details = store['dms'][dm_index]     

    return {
        'name': dm_details['name'],
        'members': dm_details['all_members']
    }
    
    
def dm_leave_v1(token, dm_id):
    store = data_store.get()
    
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]
    
    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')
    
    dm_index = check_valid_dm(dm_id, store)[1]  
    
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')    
    
    store['dms'][dm_index]['all_members'] = list(filter(lambda i: i['u_id'] != auth_user_id, store['dms'][dm_index]['all_members']))         
    
    data_store.set(store)
    
    return {}    
    
def dm_messages_v1(token, dm_id, start):
    store = data_store.get()
    
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]
    
    is_dm_valid = check_valid_dm(dm_id, store)
    if is_dm_valid == False:
        raise InputError(description='dm_id does not refer to a valid DM')    
   
    dm_index = is_dm_valid[1]
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')
    
    message_length = len(store['dms'][dm_index]['messages'])
    if start > message_length:
        raise InputError(description='start is greater than total number of messages in the DM')    
                
    end = start + 50
    if end >= message_length:
        messages_list = return_dm_messages(dm_index, start, message_length - 1, store)
        end = -1
    else:
        messages_list = return_dm_messages(dm_index, start, end, store)

    return {
        'messages': messages_list,
        'start': start,
        'end': end,
    }
    
    

def message_senddm_v1(token, dm_id, message):
    store = data_store.get()
    
    jwt_data = decode_jwt(token)    
    if check_valid_token(store, jwt_data) == False:
        raise AccessError(description='token passed in is invalid')
                
    auth_user_id = check_valid_token(store, jwt_data)[1]

    is_dm_valid = check_valid_dm(dm_id, store)
    if is_dm_valid == False:
        raise InputError(description='dm_id does not refer to a valid DM')     

    dm_index = is_dm_valid[1]
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')
    
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description='Message must be between 1 and 1000 characters inclusive')
        
    new_message_id = generate_new_message_id()
        
    current_dt = datetime.datetime.now(timezone.utc)
    utc_time = current_dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
        
    new_message = {
        'message_id': new_message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_sent': utc_timestamp
    }    
 
    store['dms'][dm_index]['messages'].append(new_message)
    
    data_store.set(store)
    
    return {
        'message_id': new_message_id
    }
