from src.data_store import data_store
from src.error import InputError, AccessError


def channels_list_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }


def channels_listall_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }


def channels_create_v1(auth_user_id, name, is_public):
    store = data_store.get()

    if len(name) < 1:
        raise InputError("Make sure channel name is more than 1 character")

    if len(name) > 20:
        raise InputError(
            "Make sure channel name does not exceed 20 characters")

    found = False
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            found = True
    if found != True:
        raise AccessError("User_id is not valid")

    new_channel_id = len(store['channels']) + 1
    new_channel = {'channel_id': new_channel_id,
                   'name': name,
                   'is_public': is_public,
                   'owner_members': [auth_user_id],
                   'all_members': [auth_user_id],
                   }
    store['channels'].append(new_channel)
    data_store.set(store)

    return {
        'channel_id': new_channel_id,
    }
