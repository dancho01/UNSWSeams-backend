from src.data_store import data_store
from src.error import InputError, AccessError

AUTH_COUNTER = 0
CHANNEL_COUNTER = 0


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
                print("++++++++++++++++++++++++++++++++++++++++++++")
                print(user['global_permissions'])
                return True
            else:
                print("++++++++++++++++++++++++++++++++++++++++++++")
                print(user['global_permissions'])
                return False


def check_owner(channel_index, auth_user_id):

    store = data_store.get()

    owner_members = store['channels'][channel_index]['owner_members']

    for owner in owner_members:
        if owner['u_id'] == auth_user_id and check_global_owner:
            return

    raise AccessError(
        'auth_user_id does not have owner permissions in the channel')


def check_already_owner(channel_index, auth_user_id):
    store = data_store.get()

    owner_members = store['channels'][channel_index]['owner_members']

    for owner in owner_members:
        if owner['u_id'] == auth_user_id and check_global_owner:
            raise InputError(
                description="u_id refers to a user who is already an owner of the channel")


def generate_user_id():
    global AUTH_COUNTER
    AUTH_COUNTER += 1
    return AUTH_COUNTER


def generate_channel_id():
    global CHANNEL_COUNTER
    CHANNEL_COUNTER += 1
    return CHANNEL_COUNTER

def reset_globals():
    global CHANNEL_COUNTER
    global AUTH_COUNTER
    CHANNEL_COUNTER = 0
    AUTH_COUNTER = 0