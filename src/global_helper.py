from src.data_store import data_store
from src.error import InputError, AccessError


def check_valid_user(u_id):
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return

    raise InputError(description="")


def check_valid_channel(c_id):
    store = data_store.get()

    found = False
    for i in range(len(store['channels'])):
        if store['channels'][i]['channel_id'] == c_id:
            found = True
            return int(i)

    if found == False:
        raise InputError(
            description="channel_id does not refer to a valid channel")


def check_authorized_user(u_id, channel_index):
    store = data_store.get()

    found = False
    for users in store['channels'][channel_index]['all_members']:
        if users['u_id'] == u_id:
            found = True

    if found == False:
        raise AccessError(
            description="channel_id is valid and the authorised user is not a member of the channel")
