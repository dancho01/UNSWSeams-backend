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
            message = create_bot_message(warning_message)
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
        message = create_bot_message(warning_message)
        store['channels'][c_dex]['messages'].append(message)
        attach_notification(user['handle_str'], warning)

        return True

    return False


def end_poll(c_dex, c_id):
    store = data_store.get()

    poll_info = store['channels'][c_dex]['poll']
    poll_status = poll_info['poll_status']
    poll_started = poll_info['start_id']

    if poll_status == False:
        warning_message = create_bot_message(format_no_vote())
        store['channels'][c_dex]['messages'].append(warning_message)
        return
    elif poll_started != c_id:
        warning_message = create_bot_message(format_no_start())
        store['channels'][c_dex]['messages'].append(warning_message)
        return

    most_popular = get_best_poll(poll_info['poll_info'])

    result = format_bot_poll(c_dex, 2) + "\n" + \
        f"The most popular choice is {most_popular}"
    bot_message = create_bot_message(result)
    store['channels'][c_dex]['messages'].append(bot_message)

    poll_info['poll_info'] = {}
    poll_info['poll_status'] = False
    poll_info['start_id'] = -1


def get_best_poll(poll_info):
    largest = 0
    largest_name = ""
    for keypair in poll_info.items():
        if len(keypair[1]) > largest:
            largest = len(keypair[1])
            largest_name = keypair[0]

    return largest_name


def get_help(c_dex):
    help_message = """
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
        Reads one option, considering that the option inputted is valid (not case sensitive).
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

    bot_message = create_bot_message(help_message)
    store['channels'][c_dex]['messages'].append(bot_message)


def add_poll_option(c_dex, options):
    store = data_store.get()

    for choice in options:
        store['channels'][c_dex]['poll']['poll_info'][choice] = []

    bot_message = create_bot_message(format_bot_poll(c_dex, 0))
    store['channels'][c_dex]['messages'].append(bot_message)


def create_poll(c_dex, question, options, c_id):
    store = data_store.get()

    if len(options) < 1:
        return False
    elif store['channels'][c_dex]['poll']['poll_status']:
        return False

    store['channels'][c_dex]['poll']['poll_status'] = True
    store['channels'][c_dex]['poll']['start_id'] = c_id
    store['channels'][c_dex]['poll']['poll_question'] = question

    for choice in options:
        store['channels'][c_dex]['poll']['poll_info'][choice] = []

    bot_message = create_bot_message(format_bot_poll(c_dex, 0))
    store['channels'][c_dex]['messages'].append(bot_message)


def create_bot_message(warning_message):
    message = {
        'message_id': - 1,
        'u_id': - 1,
        'message': warning_message,
        'time_sent': time_now(),
        'reacts': [],
        'is_pinned': False
    }

    return message


'''
    bot message formats
'''


def format_no_start():
    warning_message = "You did not start the vote!"
    return warning_message


def format_bot_warning(warnings, handle):
    warning_message = "Stop swearing @{0}! {1} more warning before timeout!!".format(
        handle, 3 - (warnings % 3))

    return warning_message


def format_bot_timeout_warning(handle, length):
    warning_message = "@{0} has been timed out for {1} seconds for profanity!".format(handle,
                                                                                      length)

    return warning_message


def format_no_vote():
    message = "There is no active poll, please do /startpoll <question> <vote1> <vote2> ..."

    return message


def format_bot_poll(c_dex, stage):
    store = data_store.get()

    poll_stats = store['channels'][c_dex]['poll']
    poll_votes = poll_stats['poll_info']

    vote_len = largest_vote_name(poll_votes)

    if stage == 0:
        poll_message = "A poll has been started\n"
    elif stage == 1:
        poll_message = "Poll in progress...\n"
    elif stage == 2:
        poll_message = "Poll has ended, these were the results\n"

    poll_message += poll_stats['poll_question'] + ":" + "\n"

    for key in poll_votes.items():
        graphics = make_vote_graphics(len(key[1]))
        poll_message += ("\t" + key[0].ljust(vote_len + 5) +
                         graphics + "\n")

    return poll_message


def make_vote_graphics(len):
    graphic = "👩 " * len

    return graphic


def largest_vote_name(poll_info):
    largest = 0
    for key in poll_info:
        if len(key) > largest:
            largest = len(key)

    return largest


'''
    voting
'''


def vote(u_id, c_dex, vote_choice):
    store = data_store.get()

    poll_status = store['channels'][c_dex]['poll']['poll_status']

    if poll_status == False:
        warning_message = create_bot_message(format_no_vote())
        store['channels'][c_dex]['messages'].append(warning_message)
        return

    poll_info = store['channels'][c_dex]['poll']['poll_info']

    if has_user_voted(poll_info, u_id):
        print("True")
        for voters in poll_info.items():
            if u_id in voters[1]:
                voters[1].remove(u_id)

            if voters[0].lower() == vote_choice.lower():
                voters[1].append(u_id)
    else:
        print("False")
        for voters in poll_info.items():
            if voters[0].lower() == vote_choice.lower():
                voters[1].append(u_id)

    bot_message = create_bot_message(format_bot_poll(c_dex, 1))
    store['channels'][c_dex]['messages'].append(bot_message)

    return


def has_user_voted(poll_info, u_id):
    for voters in poll_info.values():
        if u_id in voters:
            return True

    return False
