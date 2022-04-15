import threading
from src.data_store import data_store
from src.error import InputError, AccessError
from src.token import check_valid_token
from src.channel_helper import time_now
from src.global_helper import check_owner, check_global_owner
from src.other import clear_v1
from src.user_helper import return_user_handle
from src.commands_helper import get_user_channel_index, do_timeout, do_untimeout, warn_user, \
    command_clear_chat, create_poll, vote, end_poll, add_poll_option, get_help


def recognise_commands(token, channel_id, message):
    store = data_store.get()
    params = message.split()
    command = message.split()[0].replace("/", "").lower()
    c_id = check_valid_token(token)['u_id']
    c_handle = return_user_handle(c_id)
    c_info = get_user_channel_index(c_handle, channel_id)

    # /abot activates bot, /dbot deactivates bot
    channel_members = store['channels'][c_info['c_dex']]['owner_members']

    if command == "abot":
        if len(channel_members) != 0:
            check_owner(c_info['c_dex'], c_id)
        store['channels'][c_info['c_dex']]['bot_status'] = True
        return True
    elif command == "dbot":
        if len(channel_members) != 0:
            check_owner(c_info['c_dex'], c_id)
        store['channels'][c_info['c_dex']]['bot_status'] = False
        return True

    if store['channels'][c_info['c_dex']]['bot_status'] == False:
        raise InputError(
            description="Bot is inactive, please use /abot to activate bot")

    if command == "timeout":
        if len(params) != 3:
            raise InputError(description="Missing a parameter, please retry")
        u_info = get_user_channel_index(params[1], channel_id)
        check_owner(u_info['c_dex'], c_id)
        time_end = time_now() + int(params[2])
        do_timeout(u_info['c_dex'], u_info['u_dex'], time_end)

        t = threading.Timer(int(params[2]), do_untimeout, [
            u_info['c_dex'], u_info['u_dex']])
        t.start()
        return True
    elif command == "clearchat":
        if len(channel_members) != 0:
            check_owner(c_info['c_dex'], c_id)
        command_clear_chat(channel_id)
        return True
    elif command == "reset":
        is_global_owner(c_id)
        clear_v1()
        return True
    elif command == "startpoll":
        create_poll(c_info['c_dex'], params[1:], c_id)
        return True
    elif command == "vote":
        vote(c_id, c_info['c_dex'], params[1])
        return True
    elif command == "addpolloption":
        add_poll_option(c_info['c_dex'], params[1:])
        return True
    elif command == "endpoll":
        end_poll(c_info['c_dex'], c_id)
        return True
    elif command == "help":
        get_help(c_info['c_dex'])
        return True
    else:
        raise InputError(description="Invalid command")


def filter_language(u_id, c_dex, message):
    store = data_store.get()

    if store['channels'][c_dex]['bot_status'] == False:
        return False

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
        warn_user(c_dex, u_id)
        return True

    return False


def is_global_owner(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            if user['global_permissions'] == 1:
                return
            else:
                raise AccessError(
                    description="User is not global SEAMS owner!")
