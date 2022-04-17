from src.data_store import data_store
from src.error import InputError, AccessError
from src.token import check_valid_token
from src.channel_helper import check_message
from src.iter3_message_helper import is_user_joined, return_messages_with_query, is_message_id_valid, has_user_already_reacted, add_react_message, remove_react_message, check_invalid_message_id, is_user_reacted
from src.user_helper import create_message_react_notification


def search_v1(token, query_str):
    store = data_store.get()
    user_id = check_valid_token(token)['u_id']

    check_message(query_str)

    query_collection = []

    for channel in store['channels']:
        if is_user_joined(channel, user_id):
            query_collection = return_messages_with_query(
                query_str, channel, query_collection)

    for dm in store['dms']:
        if is_user_joined(dm, user_id):
            query_collection = return_messages_with_query(
                query_str, dm, query_collection)

    return_messages = is_user_reacted(query_collection, user_id)

    return {
        'messages': return_messages
    }


def message_react_v1(token, message_id, react_id):

    store = data_store.get()
    user_id = check_valid_token(token)['u_id']

    message = check_invalid_message_id(store, message_id, user_id)

    if react_id != 1:
        raise InputError(description='not a valid react ID')

    if has_user_already_reacted(message[0], user_id, react_id):
        raise InputError(
            description='user has already reacted to this message')

    add_react_message(user_id, message[0], react_id)

    if message[1] == 1:
        channel_id = message[2]
        dm_id = -1
    else:
        channel_id = -1
        dm_id = message[2]

    create_message_react_notification(
        channel_id, dm_id, user_id, message[0]['u_id'])

    return {}


def message_unreact_v1(token, message_id, react_id):

    store = data_store.get()
    user_id = check_valid_token(token)['u_id']

    message = check_invalid_message_id(store, message_id, user_id)

    if react_id != 1:
        raise InputError(description='not a valid react ID')

    if has_user_already_reacted(message[0], user_id, react_id) == False:
        raise InputError(description='user has not reacted to this message')

    remove_react_message(user_id, message[0], react_id)

    return {}
