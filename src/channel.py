from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()
    
    found = False 
    global_owner = False
    for user in store['users']:
        if user['id'] == auth_user_id:
            found = True 
        if user['global_permissions'] == 1:
              global_owner = True
    if found != True:
        raise AccessError("User_id is not valid")   
    
    found = False 
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            found = True 
            for member in channel['all_members']:
                if member == auth_user_id:
                    raise InputError("Authorised user is already a channel member")
            if channel['is_public'] == False and global_owner != True:               
                raise AccessError("Cannot join a private channel if not a global owner")  
            
            new_member = auth_user_id
            channel['all_members'].append(new_member)                                      
                                                     
    if found != True:
        raise InputError("Channel_id does not refer to valid channel")  
    
    data_store.set(store)
    print(store)


    return {
    }
    
