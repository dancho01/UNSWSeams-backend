import threading
from src.data_store import data_store
from src.user_helper import attach_notification
from src.channel_helper import time_now
from src.user_helper import attach_notification
from src.dm_helpers import decrement_total_num_messages_in_channel_dm


'''
timeout_helper
'''


def get_user_channel_index(handle, channel_id):
    store = data_store.get()
    for c_dex, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            for u_dex, user in enumerate(channel['all_members']):
                if user['handle_str'] == handle:
                    return {
                        'c_dex': c_dex,
                        'u_dex': u_dex
                    }


def command_clear_chat(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            decrement_total_num_messages_in_channel_dm(
                len(channel['messages']))
            channel['messages'] = []


def do_timeout(c_dex, u_dex, time_end):
    store = data_store.get()

    timed_out = store['channels'][c_dex]['all_members'][u_dex]['info']
    timed_out['timed_out_status'] = True
    timed_out['time_out_end'] = time_end


def do_untimeout(c_dex, u_dex):
    store = data_store.get()

    timed_out = store['channels'][c_dex]['all_members'][u_dex]['info']
    timed_out['timed_out_status'] = False
    timed_out['time_out_end'] = - 1


def warn_user(c_dex, u_id):
    store = data_store.get()

    for u_dex, user in enumerate(store['channels'][c_dex]['all_members']):
        if user['u_id'] == u_id:
            user['info']['warnings'] += 1
            handle = user['handle_str']
            warn_count = user['info']['warnings']
            timeout_len = user['info']['warnings'] * 20
        if user['info']['warnings'] % 3 == 0:
            # bot times them out for x amount of time
            warning_message = format_bot_timeout_warning(handle, timeout_len)
            warning = {
                'channel_id': store['channels'][c_dex]['channel_id'],
                'dm_id': -1,
                'notification_message': warning_message
            }
            message = {
                'message_id': - 1,
                'u_id': - 1,
                'message': warning_message,
                'time_sent': time_now(),
                'reacts': [],
                'is_pinned': False
            }
            store['channels'][c_dex]['messages'].append(message)
            attach_notification(handle, warning)

            do_timeout(c_dex, u_dex, time_now() + timeout_len)

            t = threading.Timer(timeout_len, do_untimeout,
                                [c_dex, u_dex])
            t.start()

            return True

        warning_message = format_bot_warning(warn_count, handle)
        warning = {
            'channel_id': store['channels'][c_dex]['channel_id'],
            'dm_id': -1,
            'notification_message': warning_message
        }
        message = {
            'message_id': - 1,
            'u_id': - 1,
            'message': warning_message,
            'time_sent': time_now(),
            'reacts': [],
            'is_pinned': False
        }
        store['channels'][c_dex]['messages'].append(message)
        attach_notification(user['handle_str'], warning)

        return True

    return False


def format_bot_warning(warnings, handle):
    warning_message = """
    Stop swearing @{0}! {1} more warning before timeout!!!
    """.format(
        handle, 3 - (warnings % 3))

    return warning_message


def format_bot_timeout_warning(handle, length):
    warning_message = "@{0} has been timed out for {1} seconds for profanity!".format(handle,
                                                                                      length)

    return warning_message
