from src.data_store import data_store
from src.error import InputError, AccessError

AUTH_COUNTER = 0
CHANNEL_COUNTER = 0
MESSAGE_ID_COUNTER = 0


def check_valid_user(u_id):
    '''
        Checks if user's id is valid
    '''
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
        if owner['u_id'] == auth_user_id and check_global_owner:
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
                'handle_str': user['handle']
            }


def messages_returned(channel_index, start, end, store):
    '''
    messages_returned takes the index, finds it and accesses the 'messages' content. It goes through
    the messages and attaces it to returned_messages until k == 50 which it will then return the
    returned_messages variable.
    '''
    returned_messages = []

    message_store = store['channels'][channel_index]['messages']

    if message_store == []:
        return returned_messages

    for message_index in range(start, end):
        returned_messages.append(message_store[message_index])

    return returned_messages


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


def generate_user_id():
    global AUTH_COUNTER
    AUTH_COUNTER += 1
    return AUTH_COUNTER


def generate_channel_id():
    global CHANNEL_COUNTER
    CHANNEL_COUNTER += 1
    return CHANNEL_COUNTER


def reset_globals():
    global CHANNEL_COUNTER, AUTH_COUNTER, MESSAGE_ID_COUNTER
    CHANNEL_COUNTER = AUTH_COUNTER = MESSAGE_ID_COUNTER = 0


def load_globals(auth, channel, message):
    global AUTH_COUNTER, CHANNEL_COUNTER, MESSAGE_ID_COUNTER
    AUTH_COUNTER = auth
    CHANNEL_COUNTER = channel
    MESSAGE_ID_COUNTER = message


def get_globals():
    global AUTH_COUNTER, CHANNEL_COUNTER, MESSAGE_ID_COUNTER

    return AUTH_COUNTER, CHANNEL_COUNTER, MESSAGE_ID_COUNTER
