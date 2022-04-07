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
