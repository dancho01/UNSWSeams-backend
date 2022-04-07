import threading
from src.data_store import data_store
from src.token import check_valid_token
from src.channel_helper import time_now
from src.standup_helper import start_standup, end_standup


def standup_start_v1(token, channel_id, length):
    auth_user_id = check_valid_token(token)['u_id']

    end_time = time_now() + length

    start_standup(channel_id, end_time)

    t = threading.Timer(length, end_standup, [channel_id, token])
    t.start()

    return {'time_finish': end_time}
