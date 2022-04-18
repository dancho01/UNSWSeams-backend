from src.data_store import data_store
from src.channel import message_send_v1
from src.error import InputError


def start_standup(channel_id, time_finish, u_id):
    """Accesses the datastore at a certain channel, activates channel by
    filling in the keypairs with args provided, resets 'standup_cache' to
    [] as a precaution and make sure the right owner of the standup owner
    is inserted

    Args:
        channel_id (int)
        time_finish (int)
        u_id (int)
    """
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['active'] = True
            channel['standup']['finish_time'] = time_finish
            channel['standup']['standup_cache'] = []
            channel['standup']['standup_owner'] = u_id


def end_standup(channel_id, token):
    """Accesses the datastore at a certain channel, deactivates channel by
    filling in the keypairs with args provided, resets 'standup_cache' to
    [] as a precaution and make sure the right owner of the standup owner
    is reset. Uses messages_send_v1 to send a formatted log of the standup.

    Args:
        channel_id (_type_)
        token (str)
    """
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            combined = combine_standup_cache(
                channel['standup']['standup_cache'])
            channel['standup']['active'] = False
            channel['standup']['finish_time'] = -1
            channel['standup']['standup_cache'] = []
            channel['standup']['standup_owner'] = None
            message_send_v1(token, channel_id, combined)


def combine_standup_cache(cache):
    """Combines a list of messages into a single string that is acts as a log
    to be sent into the channel.

    Args:
        cache (list)

    Returns:
        str: string formatted of every message in the standup cache
    """
    combined_cache = '\n'.join(cache)
    return combined_cache


def check_active(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            if channel['standup']['active']:
                return {
                    'is_active': True,
                    'time_finish': channel['standup']['finish_time']
                }
    return {
        'is_active': False,
        'time_finish': None
    }


def format_message(handle, message):
    """Takes in a message and the users handle, formats it

    Args:
        handle (str)
        message (str)

    Returns:
        str: handle: message
    """
    formatted = '{0}: {1}'.format(handle, message)

    return formatted


def add_to_standup_cache(c_id, message):
    """Takes the message, inserts the message at the start of the cache

    Args:
        c_id (int)
        message (str)
    """
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == c_id:
            channel['standup']['standup_cache'] = [
                message] + channel['standup']['standup_cache']


def check_length(length):
    """Checks if time length is valid

    Args:
        length (int)

    Raises:
        InputError: length is a negative integer
    """
    if length < 0:
        raise InputError(description="length is a negative integer")


def check_message_length(message):
    """checks to see if message is of valid length

    Args:
        message (str)

    Raises:
        InputError: length of message is over 1000 characters
    """
    if len(message) > 1000:
        raise InputError(
            description="length of message is over 1000 characters")


def check_ongoing_standup(channel_id):
    """Checks to see if there is an already active standup at the given channel_id

    Args:
        channel_id (int)

    Raises:
        InputError: an active standup is currently running in the channel
    """
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id and channel['standup']['active']:
            raise InputError(
                description="an active standup is currently running in the channel")


def check_no_standup(channel_id):
    """Checks to see if there is a lack of a standup in a specified channel

    Args:
        channel_id (int)

    Raises:
        InputError: an active standup is not currently running in the channel
    """
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id and not channel['standup']['active']:
            raise InputError(
                description="an active standup is not currently running in the channel")
