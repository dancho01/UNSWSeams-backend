from src.error import InputError, AccessError
from datetime import datetime, timezone
from src.data_store import data_store


def remove_message(message_id):
    '''
    removes the message referred to by message_id
    '''
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

    raise InputError(description="message_id does not exist")


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
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()


def get_messages(start, end_return, channel_index):
    store = data_store.get()

    return_messages = []

    for i in range(start, end_return):
        return_messages.append(
            store['channels'][channel_index]['messages'][i])

    return_messages.reverse()

    return return_messages


def edit_message(message_id, message):
    store = data_store.get()

    for channel in store['channels']:
        for messages in channel['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return

    for dm in store['dms']:
        for messages in dm['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return
