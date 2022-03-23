from src.error import InputError, AccessError
from src.data_store import check_authorization, messages_returned, data_store, check_user_registered, return_member_information
from src.channel_helper import check_message, time_now
from src.token import check_valid_token, generate_token, hash
from src.global_helper import check_valid_channel, check_authorized_user, check_already_auth, check_valid_user, check_global_owner
from src.dm import dm_leave_v1, dm_list_v1
from src.channel import messages_edit_v1, channel_leave_v1
from src.message_helper import generate_new_message_id, check_valid_message
from src.auth  import auth_logout

# use filter
def admin_user_remove_v1(token, u_id):
    auth_user_id = check_valid_token(token)['u_id']
    check_global_owner(auth_user_id)
    check_valid_user(u_id)
    store = data_store.get()
    global_owners = 0
    # check u_id is not the only global owner
    for user in store['users']:
        if check_global_owner(user['auth_user_id']):
            global_owners += 1
    
    if global_owners == 1:
        raise InputError("user you are trying to remove is the only global owner")

    # find the token for u_id
    u_id_token = generate_token(u_id)
    # for session in store['session_list']:
    #         session_id = hash(session)
        

# Edit channel messages & DM messages to "Removed user"
    # find the channels the user is in
    for channel in store['channels']:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message_id = message['message_id']
                messages_edit_v1(token, message_id, 'Removed user')
        
        # remove from channels/DMs
        channel_leave_v1(u_id_token, channel['channel_id'])


    # find the DMs the user is in
    for dms in store['dms']:
        for messages in dms['messages']:
            if messages['u_id'] == u_id:
                message_id = message['message_id']
                messages_edit_v1(u_id_token, message_id, 'Removed user')
    dm_list = dm_list_v1(u_id_token)['dms']    # dm_list is a dictionary of lists of dictionaries
    for i in range(len(dm_list)):
        dm_leave_v1(u_id_token, dm_list[i]['dm_id'])      # remove from DMs
        #for channel in store['channels']['members']:
        # channel['messages']['message_id']

# change name in data store
    # for i in range(len(store['users'])):
    #     for j in 
    #     print("++++++"")
    #     print(type(store['users']))
    #     if store['users'][i]['user_id'] == u_id:
    #         store['users'][i]['name_first'] = 'Removed'
    #         store['users'][i]['name_last'] = 'user'

    for i in range(len(store['users'])):
        if store['users'][i]['auth_user_id'] == u_id:
            store['users'][i]['name_first'] == 'Removed'
            store['users'][i]['name_last'] == 'user'


# Last step: invalidate their token (remove session list)
    auth_logout(u_id_token)
    # could just call logout for the following 2 steps:
    # loop through session list, hash each one and use check_valid_token(token)[u_id] to check what user id they are
    # if u_id matches, remove that session list, keep going until end of session list to log out every one
    data_store.set(store)
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Function: Given a user by their user ID, set their permissions to new permissions described by permission_id.
    Parameters:{ token, u_id, permission_id }
    Return Type:{}
    """
    auth_user_id = check_valid_token(token)['u_id']
    if check_global_owner(auth_user_id) == False:
        raise AccessError('authorised user is not a global owner')
    check_valid_user(u_id)
    store = data_store.get()
    global_owners = 0
    # check u_id is not the only global owner
    for user in store['users']:
        if check_global_owner(user['auth_user_id']):
            global_owners += 1
    
    if global_owners == 1:
        if check_global_owner(u_id):
            raise InputError('user you are trying to remove is the only global owner')
    if permission_id != 1 and permission_id != 2:
        raise InputError('permission_id is invalid')
    
    for user in store['users']: 
        if user['auth_user_id'] == u_id:
            if user['global_permissions'] == permission_id:
                raise InputError('the user already has the permissions level of permission_id')
            else:
                user['global_permissions'] == permission_id
                data_store.set(store)
                return {}


