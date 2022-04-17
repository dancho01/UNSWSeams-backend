from src.error import InputError, AccessError
from src.data_store import data_store
from datetime import datetime, timezone


AUTH_COUNTER = 0
CHANNEL_COUNTER = 0
MESSAGE_ID_COUNTER = 0
DM_ID_COUNTER = 0


def time_now():
    '''
    returns the current time stamp
    '''
    return int(datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp())


def check_valid_user(u_id):
    '''
        Checks if user's id is valid
    '''
    # if u_id == - 1:
    #     return

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return

    raise InputError(description="u_id does not refer to a valid user")


def check_valid_channel(c_id):
    '''
        Checks if channel id is valid 
    '''
    store = data_store.get()

    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == c_id:
            return index

    raise InputError(
        description="channel_id does not refer to a valid channel")


def check_authorized_user(u_id, channel_index):
    '''
        Checks if user is a member of the channel 
    '''
    store = data_store.get()

    for users in store['channels'][channel_index]['all_members']:
        if users['u_id'] == u_id:
            return

    raise AccessError(
        description="channel_id is valid and the authorised user is not a member of the channel")


def check_already_auth(u_id, channel_index):
    '''
        Checks if user is already a member of the channel 
    '''
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


def is_user_member(u_id, channel_index):
    store = data_store.get()

    for member in store['channels'][channel_index]['all_members']:
        if member['u_id'] == u_id:
            return

    raise InputError(
        description="u_id refers to a user who is not a member of the channel")


def check_owner(channel_index, auth_user_id):
    '''
        Checks if the user is an owner of the channel
    '''
    store = data_store.get()

    owner_members = store['channels'][channel_index]['owner_members']

    for owner in owner_members:
        if owner['u_id'] == auth_user_id and check_global_owner(auth_user_id):
            return

    raise AccessError(
        'auth_user_id does not have owner permissions in the channel')


def check_already_owner(channel_index, auth_user_id):
    '''
        Checks if the user is already the owner of a channel
    '''
    store = data_store.get()

    owner_members = store['channels'][channel_index]['owner_members']

    for owner in owner_members:
        if owner['u_id'] == auth_user_id:
            raise InputError(
                description="u_id refers to a user who is already an owner of the channel")


def return_member_information(u_id, store):
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return {
                'u_id': user['auth_user_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle'],
                'profile_img_url': user['profile_img_url'],
            }


def increment_messages_sent(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['stats']['total_messages_sent'] += 1
            num_messages_sent = user['stats']['total_messages_sent']
            user['stats']['user_stats']['messages_sent'].append({
                "num_messages_sent": num_messages_sent,
                "time_stamp": time_now()
            })


def increment_total_messages():
    store = data_store.get()
    store['stats']['total_num_messages'] += 1
    total_num_messages = store['stats']['total_num_messages']
    store['stats']['workspace_stats']['messages_exist'].append({
        'num_messages_exist': total_num_messages,
        'time_stamp': time_now()
    })


def decrement_total_messages():
    store = data_store.get()
    store['stats']['total_num_messages'] -= 1
    total_num_messages = store['stats']['total_num_messages']
    store['stats']['workspace_stats']['messages_exist'].append({
        'num_messages_exist': total_num_messages,
        'time_stamp': time_now()
    })


def generate_new_message_id():
    '''
    Generates a new message_id that is unique and sequentially increases by 1
    Args:
        None
    Return:
        Returns the next message_id
    '''
    global MESSAGE_ID_COUNTER
    MESSAGE_ID_COUNTER += 1
    return MESSAGE_ID_COUNTER


def generate_new_dm_id():
    '''
    Generates a new dm_id that is unique and sequentially increases by 1
    Args:
        None
    Return:
        Returns the next dm_id
    '''
    global DM_ID_COUNTER
    DM_ID_COUNTER += 1
    return DM_ID_COUNTER


def generate_user_id():
    global AUTH_COUNTER
    AUTH_COUNTER += 1
    return AUTH_COUNTER


def generate_channel_id():
    global CHANNEL_COUNTER
    CHANNEL_COUNTER += 1
    return CHANNEL_COUNTER


def reset_globals():
    global CHANNEL_COUNTER, AUTH_COUNTER, MESSAGE_ID_COUNTER, DM_ID_COUNTER
    CHANNEL_COUNTER = AUTH_COUNTER = MESSAGE_ID_COUNTER = DM_ID_COUNTER = 0


def load_globals(auth, channel, message, dm):
    global CHANNEL_COUNTER, AUTH_COUNTER, MESSAGE_ID_COUNTER, DM_ID_COUNTER
    AUTH_COUNTER = auth
    CHANNEL_COUNTER = channel
    MESSAGE_ID_COUNTER = message
    DM_ID_COUNTER = dm


def get_globals():
    global CHANNEL_COUNTER, AUTH_COUNTER, MESSAGE_ID_COUNTER, DM_ID_COUNTER

    return CHANNEL_COUNTER, AUTH_COUNTER, MESSAGE_ID_COUNTER, DM_ID_COUNTER
