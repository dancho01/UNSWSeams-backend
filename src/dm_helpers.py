DM_ID_COUNTER = 0

def generate_new_dm_id():
    global DM_ID_COUNTER
    DM_ID_COUNTER += 1
    return DM_ID_COUNTER
    

def check_for_duplicates_uids(u_ids):
    unique_ids = set(u_ids)
    if len(u_ids) == len(unique_ids):
        return False
    else:
        return True

def return_handle(u_id, store):
    for user_index in range(len(store['users'])):
        if store['users'][user_index]['auth_user_id'] == u_id:
            return store['users'][user_index]['handle']
            
def check_valid_dm(dm_id, store):
    for dm_index in range(len(store['dms'])):
        if store['dms'][dm_index]['dm_id'] == dm_id:
            return True, dm_index     
    return False   
    
def check_user_member_dm(u_id, store, dm_index):
    for member in store['dms'][dm_index]['all_members']:
        if u_id == member['u_id']:
            return True
    return False
    
def return_dm_messages(dm_index, start, end, store):
    returned_messages = []
    
    
    message_store = store['dms'][dm_index]['messages']

    if message_store == []:
        return returned_messages

    for message_index in range(start, end):
        returned_messages.append(message_store[message_index])

    return returned_messages
