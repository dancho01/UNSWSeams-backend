DM_ID_COUNTER = 0

def generate_new_dm_id():
    '''
    Generates a new dm_id that is unique and sequentially increases by 1
    Args:
        None
    Return:
        Returns the next dm_id
    '''
    global DM_ID_COUNTER
    DM_ID_COUNTER += 1
    return DM_ID_COUNTER
    

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
            return store['users'][user_index]['handle']
            
            
def generate_DM_name(auth_user_id, u_ids, store):
    '''
    
    '''
    list_handles = []
    for u_id in u_ids:
        list_handles.append(return_handle(u_id, store))
        
    list_handles.append(return_handle(auth_user_id, store))
        
    ordered_handles = sorted(list_handles)
    name = ', '.join(ordered_handles)
            
            
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
    for dm_index in range(len(store['dms'])):
        if store['dms'][dm_index]['dm_id'] == dm_id:
            return True, dm_index     
    return False   
    
    
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
    for member in store['dms'][dm_index]['all_members']:
        if u_id == member['u_id']:
            return True
    return False
    
    
def return_dm_messages(dm_index, start, end, store):
    '''
    Returns a list of messages between the 'start' and 'end' indices
    Args:
        dm_index    int             the index position of the DM within list of DMs
        start       int             the starting index 
        end         int             the end index
        store       dict            the copy of the data structure 
    Return:
        - Returns the list of messages that were appended between the two indices      
    '''
    returned_messages = []
        
    message_store = store['dms'][dm_index]['messages']

    if message_store == []:
        return returned_messages

    for message_index in range(start, end):
        returned_messages.append(message_store[message_index])

    return returned_messages
