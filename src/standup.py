import threading
from src.data_store import data_store
from src.token import check_valid_token
from src.channel_helper import time_now
from src.user_helper import return_user_handle
from src.global_helper import check_valid_channel, check_authorized_user
from src.standup_helper import start_standup, end_standup, check_active, format_message, \
    add_to_standup_cache, check_length, check_message_length, check_no_standup, check_ongoing_standup


def standup_start_v1(token, channel_id, length):
    """After passing error checks, calls start standup to initialise the standup
    in that channel, then after length amount of time called end startup to conclude
    the session.

    Args:
        token (str)
        channel_id (int)
        length (int)

    Returns:
        struct: struct with ending time attached to the key 'time_finish'
    """
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_length(length)
    check_authorized_user(user_id, channel_index)
    check_ongoing_standup(channel_id)

    end_time = time_now() + length

    start_standup(channel_id, end_time, user_id)

    t = threading.Timer(length, end_standup, [channel_id, token])
    t.start()

    return {'time_finish': end_time}


def standup_active_v1(token, channel_id):
    """Finds the channel index after error checks, looks at if
    standup is active within the channel

    Args:
        token (str)
        channel_id (int)

    Returns:
        bool: true if there is active standup, else false
    """
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)

    active_status = check_active(channel_id)
    return active_status


def standup_send_v1(token, channel_id, message):
    """Formats the standup, and sends it once it is over

    Args:
        token (str)
        channel_id (int)
        message (str)

    Returns:
        dict: empty_dict
    """
    user_id = check_valid_token(token)['u_id']
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)
    check_message_length(message)
    check_no_standup(channel_id)

    user_handle = return_user_handle(user_id)

    formatted_message = format_message(user_handle, message)

    add_to_standup_cache(channel_id, formatted_message)
    return {}
