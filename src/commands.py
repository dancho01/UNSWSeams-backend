import threading
from src.data_store import data_store
from src.error import InputError, AccessError
from src.token import check_valid_token
from src.channel_helper import time_now
from src.global_helper import check_owner, check_global_owner
from src.other import clear_v1
from src.user_helper import return_user_handle
from src.commands_helper import get_user_channel_index, do_timeout, do_untimeout, warn_user, \
    command_clear_chat, create_poll, vote, end_poll, add_poll_option, get_help, create_bot_message, \
    check_command_owner_status


def recognise_commands(token, channel_id, message):
    """
        Recognises that the user is implementing a command, there are a range of commands:

        Here is a list of commands available:

    /abot
    Description
        Activates the bot, if channel has no owners then bot can be activated by anyone
    Args
        - None

    /dbot
    Description
        Deactivates the bot
    Args
        - None

    /timeout <targethandle> <length>
    Description
        Times out the user whos handle is specified for an specified length.
    Args
        - targethandle is the handle of the user you want to time out
        - length is the time of the timeout in seconds

    /clearchat
    Description
        Clears the chat of the server it is used in.
    Args
        None

    /reset
    Description
        THIS IS ONLY TO  BE USED BY GLOBAL OWNERS, it serves as a hard reset.
    Args
        None

    /startpoll <question> <option1> <option2> ...
    Description
        Initiates a poll in the specified server, will read as many options as inputted.
        First argument will be considered the question
    Args
        - question 
        - option (as many as needed)

    /addpolloption <option1> <option2> ...
    Description
        Adds options to existing poll, will read as many options as inputted
    Args
        - option (as many as needed) 

    /vote <option>
    Description
        Reads one option, considering that the option inputted is valid (case sensitive).
        A user can only choose 1 option.
    Args
        - option

    /endpoll
    Description
        Ends existing poll.
    Args
        - None
    """
    store = data_store.get()
    params = message.split()
    command = message.split()[0].replace("/", "").lower()
    c_id = check_valid_token(token)['u_id']
    c_handle = return_user_handle(c_id)
    c_info = get_user_channel_index(c_handle, channel_id)

    # /abot activates bot, /dbot deactivates bot
    channel_members = store['channels'][c_info['c_dex']]['all_members']
    channel_owners = store['channels'][c_info['c_dex']]['owner_members']
    if command == "abot":

        if len(channel_owners) != 0:
            check_command_owner_status(c_info['c_dex'], c_id)
        store['channels'][c_info['c_dex']]['bot_status'] = True
        return True
    elif command == "dbot":
        if len(channel_owners) != 0:
            check_command_owner_status(c_info['c_dex'], c_id)
        store['channels'][c_info['c_dex']]['bot_status'] = False
        return True

    if store['channels'][c_info['c_dex']]['bot_status'] == False:
        raise InputError(
            description="Bot is inactive, please use /abot to activate bot")

    if command == "timeout":
        if len(params) != 3:
            raise InputError(description="Missing a parameter, please retry")
        u_info = get_user_channel_index(params[1], channel_id)
        check_command_owner_status(u_info['c_dex'], c_id)
        time_end = time_now() + int(params[2])
        do_timeout(u_info['c_dex'], u_info['u_dex'], time_end)

        t = threading.Timer(int(params[2]), do_untimeout, [
            u_info['c_dex'], u_info['u_dex']])
        t.start()
        return True
    elif command == "clearchat":
        if len(channel_owners) != 0:
            check_command_owner_status(c_info['c_dex'], c_id)
        command_clear_chat(channel_id)
        return True
    elif command == "reset":
        is_global_owner(c_id)
        clear_v1()
        return True
    elif command == "startpoll":
        if len(params) < 4:
            message = "Missing parameters, please do /startpoll <question> <option1> <option2>.."
            bot_message = create_bot_message(message)
            store['channels'][c_info['c_dex']]['messages'].append(bot_message)
            raise InputError(
                description="Not enough arguments!")

        create_poll(c_info['c_dex'], params[1], params[2:], c_id)
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
    '''
        Checks for any swear words listed in swear_words list,
        return True means a swear word exists, otherwise False.
    '''
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
    '''
        Different variation of check_global_owner, instead of returning bool
        it simply raises an error if requirements are not met
    '''
    store = data_store.get()
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            if user['global_permissions'] == 1:
                return
            else:
                raise AccessError(
                    description="User is not global SEAMS owner!")
