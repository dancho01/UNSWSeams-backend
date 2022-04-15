import threading
from src.data_store import data_store
from src.error import InputError
from src.token import check_valid_token
from src.channel_helper import time_now
from src.global_helper import check_owner
from src.commands_helper import get_user_channel_index, do_timeout, do_untimeout, warn_user


def recognise_commands(token, channel_id, message):

    params = message.split()
    print("--------------")
    print(params)
    command = message.split()[0].replace("/", "")
    commander_id = check_valid_token(token)['u_id']

    # should be /timeout targethandle length(in seconds)
    if command == "timeout":
        if len(params) != 3:
            raise InputError(description="Missing a parameter, please retry")

        u_info = get_user_channel_index(params[1], channel_id)
        check_owner(u_info['c_dex'], commander_id)
        time_end = time_now() + int(params[2])
        do_timeout(u_info['c_dex'], u_info['u_dex'], time_end)

        t = threading.Timer(int(params[2]), do_untimeout, [
                            u_info['c_dex'], u_info['u_dex']])
        t.start()

        return True

    raise InputError(description="Invalid command")


def filter_language(u_id, c_index, message):
    swear_words = ['fuck',
                   'shit',
                   'cunt',
                   'dick',
                   'arsehole',
                   'bullshit',
                   'bitch',
                   'tit',
                   'prick',
                   'twat',
                   'pussy',
                   'cock',
                   'dickhead',
                   'motherfucker']

    if (any(ele in message.lower() for ele in swear_words)):
        warn_user(c_index, u_id)
