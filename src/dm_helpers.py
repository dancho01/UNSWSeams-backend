from datetime import timezone
import datetime
from src.data_store import data_store
from src.channel_helper import time_now
from src.error import InputError, AccessError
from src.global_helper import increment_total_messages, increment_messages_sent


def check_for_duplicates_uids(u_ids):
    '''
    Checks if there are any duplicate user ids within the list
    Args:
        u_ids       list of int     a list of the different u_ids
    Return:
        - Returns True if there are duplicate u_ids in the list_dms
        - Returns False if the u_ids are all unique  
    '''

    unique_ids = set(u_ids)
    if len(u_ids) == len(unique_ids):
        return False
    else:
        return True


def return_handle(u_id, store):
    '''
    Given a user id, returns back their respective handle
    Args:
        u_id        int             the id of the user 
        store       dict            the copy of the data structure 
    Return:
        Returns the user's handle             
    '''
    for user_index in range(len(store['users'])):
        if store['users'][user_index]['auth_user_id'] == u_id:
            found_user = user_index
    return store['users'][found_user]['handle']


def generate_DM_name(auth_user_id, u_ids, store):
    '''
    Given the u_ids of all the members in the DM, generates a name for the DM 
    based on their handles 
    Args:
        auth_user_id    int         the id of authorised user
        u_ids           list        a list of ids of the other members 
        store           dict        the copy of the data structure 
    Return:
        Returns the name of the DM

    '''
    list_handles = []
    for u_id in u_ids:
        list_handles.append(return_handle(u_id, store))

    list_handles.append(return_handle(auth_user_id, store))

    ordered_handles = sorted(list_handles)
    name = ', '.join(ordered_handles)

    return name


def check_valid_dm(dm_id, store):
    '''
    Checks if the dm_id passed in refers to a valid DM
    Args:
        dm_id       int             the id of the dm
        store       dict            the copy of the data structure
    Return:
        - Returns False if dm_id does not refer to a valid DM 
        - Returns True if dm_id is valid and also returns its index position
        for easier lookup in the future    
    '''

    for dm_dex, dm in enumerate(store['dms']):
        if dm['dm_id'] == dm_id:
            return dm_dex

    raise InputError(description='dm_id does not refer to a valid DM')


def check_user_member_dm(u_id, store, dm_index):
    '''
    Checks if the authorised user is a member of the DM
    Args:
        u_id        int             the id of the user
        store       dict            the copy of the data structure
        dm_index    int             the index position of the DM within a list of DMs
    Return:
        - Returns False if user is not a member of the DM
        - Returns True if user is a member of the DM
    '''
    found = False
    for member in store['dms'][dm_index]['all_members']:
        if u_id == member['u_id']:
            found = True
    if found != True:
        raise AccessError(description='authorised user is not member of DM')

def increment_user_dms_joined(auth_user_id):
    '''
    Increases the number of dms joined by the user in user_stats by 1
    Args:
        auth_user_id        int             the id of the user

    Return:
        None
    '''
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['stats']['total_dms_joined'] += 1
            num_dms_joined = user['stats']['total_dms_joined']
            user['stats']['user_stats']['dms_joined'].append({
                "num_dms_joined": num_dms_joined,
                "time_stamp": time_now()
            })


def decrement_user_dms_joined(auth_user_id):
    '''
    Decreases the number of dms joined by the user in user_stats by 1
    Args:
        auth_user_id        int             the id of the user

    Return:
        None
    '''
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['stats']['total_dms_joined'] -= 1
            num_dms_joined = user['stats']['total_dms_joined']
            user['stats']['user_stats']['dms_joined'].append({
                "num_dms_joined": num_dms_joined,
                "time_stamp": time_now()
            })


def increment_total_num_dms():
    '''
    Increases the total number of dms that exist in the server in workspace_stats by 1
    Args:
        None
    Return:
        None
    '''
    store = data_store.get()
    store['stats']['total_num_dms'] += 1
    num_dms_exist = store['stats']['total_num_dms']
    store['stats']['workspace_stats']['dms_exist'].append({
        'num_dms_exist': num_dms_exist,
        'time_stamp': time_now()
    })


def decrement_total_num_dms():
    '''
    Decreases the total number of dms that exist in the server in workspace_stats by 1
    Args:
        None
    Return:
        None
    '''
    store = data_store.get()
    store['stats']['total_num_dms'] -= 1
    num_dms_exist = store['stats']['total_num_dms']
    store['stats']['workspace_stats']['dms_exist'].append({
        'num_dms_exist': num_dms_exist,
        'time_stamp': time_now()
    })


def decrement_total_num_messages_in_channel_dm(num_msgs_in_dm):
    '''
    Decreases the total number of messages that exist in the server in workspace_stats by 1
    Args:
        None
    Return:
        None
    '''
    store = data_store.get()
    store['stats']['total_num_messages'] -= num_msgs_in_dm
    if num_msgs_in_dm != 0:
        total_num_messages = store['stats']['total_num_messages']
        store['stats']['workspace_stats']['messages_exist'].append({
            'num_messages_exist': total_num_messages,
            'time_stamp': time_now()
        })


def store_message_send_dm_message(dm_index, new_message, auth_user_id):
    '''
    Increases the total number of dms that exist in the server in workspace_stats by 1. 
    Increases the number of messages sent by the user by 1. 
    Sends the message into the dm. 
    Args:
        auth_user_id    int         the id of authorised user
        dm_index        int         the index of the dm 
        new_message     string      the new message to send in the dm 
    Return:
        None
    '''
    store = data_store.get()
    increment_messages_sent(auth_user_id)
    increment_total_messages()
    store['dms'][dm_index]['messages'].append(new_message)

