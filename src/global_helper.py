from src.data_store import data_store
from src.error import InputError, AccessError


def check_valid_user(u_id):
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return

    raise InputError(description="")


def check_valid_channel_user(c_id, u_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == c_id:
            if check_authorized_user(channel['all_members'], u_id) == True:
                return True
            else:
                raise AccessError(
                    description="channel_id is valid and the authorised user is not a member of the channel")

    raise InputError(
        description="channel_id does not refer to a valid channel")


def check_authorized_user(channel_auth_list, u_id):
    for user in channel_auth_list:
        if user['auth_user_id'] == u_id:
            return True

    return False
