from src.data_store import data_store
from src.channel import message_send_v1


def start_standup(channel_id, time_finish):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['active'] = True
            channel['standup']['finish_time'] = time_finish


def end_standup(channel_id, token):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            combined = combine_standup_cache(
                channel['standup']['standup_cache'])
            message_send_v1(token, channel_id, combined)
            channel['standup']['active'] = False
            channel['standup']['finish_time'] = -1
            channel['standup']['standup_cache'] = []


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
            else:
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
