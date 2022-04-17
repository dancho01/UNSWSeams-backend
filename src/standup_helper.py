from src.data_store import data_store
from src.channel import message_send_v1
from src.error import InputError


def start_standup(channel_id, time_finish, u_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['active'] = True
            channel['standup']['finish_time'] = time_finish
            channel['standup']['standup_cache'] = []
            channel['standup']['standup_owner'] = u_id


def end_standup(channel_id, token):
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
    formatted = '{0}: {1}'.format(handle, message)

    return formatted


def add_to_standup_cache(c_id, message):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == c_id:
            channel['standup']['standup_cache'] = [
                message] + channel['standup']['standup_cache']


def check_length(length):
    if length < 0:
        raise InputError(description="length is a negative integer")


def check_message_length(message):
    if len(message) > 1000:
        raise InputError(
            description="length of message is over 1000 characters")


def check_ongoing_standup(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id and channel['standup']['active']:
            raise InputError(
                description="an active standup is currently running in the channel")


def check_no_standup(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id and not channel['standup']['active']:
            raise InputError(
                description="an active standup is not currently running in the channel")
