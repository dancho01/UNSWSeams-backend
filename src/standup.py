import threading
from src.data_store import data_store
from src.token import check_valid_token
from src.channel_helper import time_now
from src.user_helper import return_user_handle
from src.global_helper import check_valid_channel, check_authorized_user
from src.standup_helper import start_standup, end_standup, check_active, format_message, \
    add_to_standup_cache, check_length, check_message_length, check_no_standup, check_ongoing_standup


def standup_start_v1(token, channel_id, length):
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_length(length)
    check_authorized_user(user_id, channel_index)
    check_ongoing_standup(channel_id)

    end_time = time_now() + length

    start_standup(channel_id, end_time)

    t = threading.Timer(length, end_standup, [channel_id, token])
    t.start()

    return {'time_finish': end_time}


def standup_active_v1(token, channel_id):
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)

    active_status = check_active(channel_id)
    return active_status


def standup_send_v1(token, channel_id, message):
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)
    check_message_length(message)
    check_no_standup(channel_id)

    user_handle = return_user_handle(user_id)

    formatted_message = format_message(user_handle, message)

    add_to_standup_cache(channel_id, formatted_message)
    return {}
