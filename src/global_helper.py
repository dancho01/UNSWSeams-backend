from src.data_store import data_store
from src.error import InputError, AccessError


def check_valid_user(u_id):
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return

    raise InputError(description="u_id does not refer to a valid user")


def check_valid_channel(c_id):
    store = data_store.get()

    for i in range(len(store['channels'])):
        if store['channels'][i]['channel_id'] == c_id:
            return int(i)

        raise InputError(
            description="channel_id does not refer to a valid channel")


def check_authorized_user(u_id, channel_index):
    store = data_store.get()

    found = False
    for users in store['channels'][channel_index]['all_members']:
        if users['u_id'] == u_id:
            found = True
            break

    if found == False:
        raise AccessError(
            description="channel_id is valid and the authorised user is not a member of the channel")

    return


def check_already_auth(u_id, channel_index):
    store = data_store.get()

    for users in store['channels'][channel_index]['all_members']:
        if users['u_id'] == u_id:
            raise InputError(
                description="u_id refers to a user who is already a member of the channel")

    return

def check_global_owner(auth_user_id):
    """
        takes a user_id and returns true if global owner, else false if not global owner
    """
    store = data_store.get()
    for user in store['users']: 
        if user['auth_user_id'] == auth_user_id:
            if user['global_permissions'] == 1:
                return True
            else:
                return False
    
