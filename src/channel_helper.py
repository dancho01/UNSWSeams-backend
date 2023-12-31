from src.error import InputError, AccessError
from datetime import datetime, timezone
from src.global_helper import decrement_total_messages, increment_total_messages, increment_messages_sent
from src.data_store import data_store


def find_message_channel_index(message_id):
    '''
    Gets message id and returns the index of the channel it is in
    '''
    store = data_store.get()

    for c_dex, channel in enumerate(store['channels']):
        for message in channel['messages']:
            if message['message_id'] == message_id:
                to_return = c_dex

    return to_return


def message_in_channels(message_id):
    '''
    Checks if the message that is being request resides within channels and not dms
    '''
    store = data_store.get()
    for _, channel in enumerate(store['channels']):
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return True

    return False


def check_timed_out(c_dex, user_id):
    '''
    Checks if a user is currently timed out in a channel
    '''
    store = data_store.get()

    for user in store['channels'][c_dex]['all_members']:
        if user['u_id'] == user_id and user['info']['timed_out_status']:
            time_left = user['info']['time_out_end'] - time_now()
            raise AccessError(
                description=f"You have been timed out, there is {time_left} seconds left")


def remove_message(message_id):
    '''
    removes the message referred to by message_id
    '''
    store = data_store.get()

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                decrement_total_messages()
                channel['messages'].remove(message)
                return

    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                decrement_total_messages()
                dm['messages'].remove(message)
                # return

    # raise InputError(description="message_id does not exist")


def member_leave(u_id, channel_index):
    '''
    removes a user u_id from a channel referred to by channel_index
    '''
    store = data_store.get()

    store['channels'][channel_index]['all_members'] = list(filter(
        lambda x: x['u_id'] != u_id, store['channels'][channel_index]['all_members']))

    store['channels'][channel_index]['owner_members'] = list(filter(
        lambda x: x['u_id'] != u_id, store['channels'][channel_index]['owner_members']))


def check_message(message):
    '''
    check the length of a message is not empty nor over 1000 characters
    '''
    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='length of message is less than 1 or over 1000 characters')


def time_now():
    '''
    returns the current time stamp
    '''
    return int(datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp())


def get_messages(start, end_return, channel_index):
    '''
    Gets messages from start index to end
    '''
    store = data_store.get()

    return_messages = []

    for i in range(start, end_return):
        return_messages.append(
            store['channels'][channel_index]['messages'][i])

    return_messages.reverse()

    return return_messages


def edit_message(message_id, message):
    '''
    Alter the message at message_id and replace with message
    '''
    store = data_store.get()

    for channel in store['channels']:
        for messages in channel['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message

    for dm in store['dms']:
        for messages in dm['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message


'''
    message_send
'''


def send_message(new_message, channel_id, user_id):
    """Sends the message attached to a channel and increments stats

    Args:
        new_message (str)
        channel_id (int)
        user_id (int)
    """
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)
    increment_messages_sent(user_id)
    increment_total_messages()


def send_dm(new_message, dm_id, user_id):
    store = data_store.get()
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            dm['messages'].append(new_message)
    increment_messages_sent(user_id)
    increment_total_messages()


def create_message(new_message_id, user_id, message):
    new_message = {
        'message_id': new_message_id,
        'u_id': user_id,
        'message': message,
        'time_sent': time_now(),
        'reacts': [],
        'is_pinned': False
    }

    return new_message


'''
    message_share_helpers
'''


def check_valid_message_or_dm(og, c_id, dm_id, u_id):
    '''
        Checks whether c_id and dm_id have a valid combination
    '''
    if c_id == -1 and dm_id == -1:
        raise InputError(description='Channel_id and dm_id are -1')
    elif c_id != -1 and dm_id != -1:
        raise InputError(description='Neither channel_id or dm_id are -1')

    store = data_store.get()

    if dm_id == -1:
        # dm_id == -1 means the message resides in channels
        return check_message_in_channels(og, u_id, store)
    else:
        # c_id == -1 means the message resides within dms
        return check_message_in_dms(og, u_id, store)


def check_message_in_channels(og, u_id, store):
    '''
        Checks if the message exists in all channels and ensures the user has permissions
    '''
    for channels in store['channels']:
        for message in channels['messages']:
            if message['message_id'] == og and member_check(u_id, channels):
                return message['message']

    raise InputError(description='This message is not found in channels')


def check_message_in_dms(og, u_id, store):
    '''
        Checks if the message exists in all dms and ensures the user has permissions
    '''
    for dms in store['dms']:
        for message in dms['messages']:
            if message['message_id'] == og and member_check(u_id, dms):
                return message['message']

    raise InputError(description='This message is not found in dms')


def member_check(u_id, channel):
    '''
        Checks if this member has access to the channel in which the message is located
    '''
    for member in channel['all_members']:
        if member['u_id'] == u_id:
            return True

    raise AccessError(
        description='the pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid) \
                    and the authorised user has not joined the channel or DM they are trying to share \
                    the message to')


def share_message_format(to_share, message):

    formatted = "Shared message:\n{0}\nAdditional message:\n{1}".format(
        to_share, message)

    return formatted


def increment_user_channels_joined(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['stats']['total_channels_joined'] += 1
            num_channels_joined = user['stats']['total_channels_joined']
            user['stats']['user_stats']['channels_joined'].append({
                "num_channels_joined": num_channels_joined,
                "time_stamp": time_now()
            })


def decrement_user_channels_joined(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['stats']['total_channels_joined'] -= 1
            num_channels_joined = user['stats']['total_channels_joined']
            user['stats']['user_stats']['channels_joined'].append({
                "num_channels_joined": num_channels_joined,
                "time_stamp": time_now()
            })


def check_standup_owner(u_id, c_dex):
    """Checks if the owner who is indicated at u_id is the started of a standup,
    if so they cannot leave the channel until the standup is over.

    Args:
        u_id (int)
        c_dex (int)

    Raises:
        InputError: the authorised user is the starter of an active standup in the channel_
    """
    store = data_store.get()

    standup_info = store['channels'][c_dex]['standup']

    if standup_info['active']:
        if standup_info['standup_owner'] != u_id:
            raise InputError(
                description="the authorised user is the starter of an active standup in the channel")
