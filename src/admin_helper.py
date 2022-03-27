from src.data_store import data_store
from src.global_helper import check_global_owner
from src.error import InputError
from src.token import hash


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


def only_global_owner_check(u_id):
    store = data_store.get()
    global_owners = 0

    for user in store['users']:
        if check_global_owner(user['auth_user_id']):
            global_owners += 1
        if user['auth_user_id'] == u_id:
            u_profile = user

    if global_owners == 1 and u_profile['global_permissions'] == 1:
        raise InputError(
            'user you are trying to remove is the only global owner')

    return


def remove_from_session_list(u_id):
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id and hash(str(u_id) + user['handle']) in store['session_list']:
            store['session_list'].remove(
                hash(str(u_id) + user['handle']))

    return

def check_and_set_new_permissions(u_id, permission_id):
    store = data_store.get()

    for i in range(len(store['users'])):
        if store['users'][i]['auth_user_id'] == u_id:
            if store['users'][i]['global_permissions'] == permission_id:
                raise InputError(
                    'the user already has the permissions level of permission_id')
            else:
                store['users'][i]['global_permissions'] = permission_id
                data_store.set(store)
                return {}