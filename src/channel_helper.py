from src.error import InputError, AccessError
from datetime import datetime, timezone
from src.data_store import data_store


def remove_message(message_id):

    store = data_store.get()

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                channel['messages'].remove(message)
                data_store.set(store)
                return

    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm['messages'].remove(message)
                data_store.set(store)
                return


def member_leave(u_id, channel_index):
    store = data_store.get()

    store['channels'][channel_index]['all_members'] = list(filter(
        lambda x: x['u_id'] != u_id, store['channels'][channel_index]['all_members']))

    store['channels'][channel_index]['owner_members'] = list(filter(
        lambda x: x['u_id'] != u_id, store['channels'][channel_index]['owner_members']))


def check_message(message):
    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='length of message is less than 1 or over 1000 characters')


def time_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()