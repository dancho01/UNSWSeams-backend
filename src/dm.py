from src.error import InputError, AccessError
from src.data_store import data_store, return_member_information, check_user_registered
from src.token import check_valid_token
from src.dm_helpers import check_for_duplicates_uids, return_handle, check_valid_dm, check_user_member_dm, generate_new_dm_id, generate_DM_name
from src.message_helper import generate_new_message_id
from datetime import timezone
import datetime


# DM Functions/Implementation details
def dm_create_v1(token, u_ids):
    '''
    Creates a new DM where the members are the creator of this DM and the users
    that it was directed to. The name of the DM is generated based on the users' handles.
    The new DM is added to the list of all DMs

    Args:
        token       str             the encoded JWT string to verify user
        u_ids       list            a list of users the DM is directed to  
    Exceptions:
        InputError      occurs when any u_id in the list does not refer to valid user
        InputError      occurs when there are any duplicate u_ids in the list

    Return:
        Returns a dictionary with the key 'dm_id', the DM's new id           
    '''
    store = data_store.get()

    # checks whether the token is valid and verifies user
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    # InputError raised if any u_id is not valid
    for u_id in u_ids:
        if check_user_registered(u_id, store) == False:
            raise InputError(
                description='one of the user ids does not refer to valid user')

    # InputError raised if any duplicate u_ids exist
    if check_for_duplicates_uids(u_ids) == True:
        raise InputError(description='duplicate user ids not allowed')

    new_dm_id = generate_new_dm_id()

    name = generate_DM_name(auth_user_id, u_ids, store)

    new_dm = {'dm_id': new_dm_id,
              'name': name,
              'all_members': [],
              'messages': [],
              }

    # adding owner to all_members list
    new_dm['all_members'].append(
        return_member_information(auth_user_id, store))

    # adding the rest of users to all_members list
    for u_id in u_ids:
        new_dm['all_members'].append(return_member_information(u_id, store))

    # only original creator of DM is added to owner
    new_dm['owner'] = return_member_information(auth_user_id, store)

    store['dms'].append(new_dm)
    data_store.set(store)

    return {
        'dm_id': new_dm_id,
    }


def dm_list_v1(token):
    store = data_store.get()
    '''
    Returns the list of DMs that the user is a member of
    
    
    
    Args:
        token       str             the encoded JWT string to verify user
        u_ids       list            a list of users the DM is directed to  
    Exceptions:
        InputError      occurs when any u_id in the list does not refer to valid user
        InputError      occurs when there are any duplicate u_ids in the list

    Return:
        Returns a dictionary with the key 'dm_id', the DM's new id   
    
    
    '''
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

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

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

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


def dm_details_v1(token, dm_id):
    store = data_store.get()

    # checks if token is valid, verifying user
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

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

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']
    
    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    store['dms'][dm_index]['all_members'] = list(filter(
        lambda i: i['u_id'] != auth_user_id, store['dms'][dm_index]['all_members']))

    return {}


def dm_messages_v1(token, dm_id, start):
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']
 
    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]
    
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    message_length = len(store['dms'][dm_index]['messages'])

    if start > message_length:
        raise InputError(
            description='start is greater than total number of messages in the DM')

    elif start + 49 <= message_length:
        end_return = end = start + 50
    else:
        end_return = message_length
        end = -1

    return_messages = []

    for i in range(start, end_return):
        return_messages.append(
            store['dms'][dm_index]['messages'][i])

    return {
        'messages': return_messages,
        'start': start,
        'end': end,
    }


def message_senddm_v1(token, dm_id, message):
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]
    
    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='Message must be between 1 and 1000 characters inclusive')

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
