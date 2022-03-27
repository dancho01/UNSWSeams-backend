from src.data_store import data_store
from src.channel_helper import check_message, member_leave
from src.message_helper import check_valid_message


def remove_user_name(u_id):

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['name_first'] = "Removed"
            user['name_last'] = "user"
            user['active'] = False
    data_store.set(store)

    return {}


def remove_user_messages(u_id):
    store = data_store.get()

    for channel in store['channels']:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = "Removed user"

    for dms in store['dms']:
        for message in dms['messages']:
            if message['u_id'] == u_id:
                message['message'] = "Removed user"
    
    data_store.set(store)
    return {}


def remove_user_from_channels(u_id):

    store = data_store.get()

    for channel in store['channels']:
        for owner_member in channel['owner_members']:
            if owner_member['u_id'] == u_id:
                channel['owner_members'].remove(owner_member)
                

        for all_member in channel['all_members']:
            if all_member['u_id'] == u_id:
                channel['all_members'].remove(all_member)

    for dm in store['dms']:
        for member in dm['all_members']:
            if member['u_id'] == u_id:
                dm['all_members'].remove(member)


    