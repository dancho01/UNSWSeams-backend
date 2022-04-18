import threading
from src.data_store import data_store
from src.error import InputError, AccessError
from src.user_helper import attach_notification
from src.channel_helper import time_now
from src.user_helper import attach_notification
from src.dm_helpers import decrement_total_num_messages_in_channel_dm
from src.global_helper import check_global_owner


def get_help(c_dex):
    '''
        List of commands the bot sends
    '''
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

    bot_message = create_bot_message(help_message)
    store['channels'][c_dex]['messages'].append(bot_message)


'''
timeout_helper
'''


def get_user_channel_index(handle, channel_id):
    '''
        Finds the channel index and user index of a certain user within a certain
        channel_id.
    '''
    store = data_store.get()
    for c_dex, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            for u_dex, user in enumerate(channel['all_members']):
                if user['handle_str'] == handle:
                    to_return = {
                        'c_dex': c_dex,
                        'u_dex': u_dex
                    }

    return to_return


def do_timeout(c_dex, u_dex, time_end):
    '''
        Sets a users 'time_out_status' to True, which means they cannot edit,
        delete or send messages
    '''
    store = data_store.get()

    timed_out = store['channels'][c_dex]['all_members'][u_dex]['info']
    timed_out['timed_out_status'] = True
    timed_out['time_out_end'] = time_end


def do_untimeout(c_dex, u_dex):
    '''
        Sets a users 'time_out_status' to False, meaning they are able to edit, delete
        and send messages.
    '''
    store = data_store.get()

    store['channels'][c_dex]['all_members'][u_dex]['info']['timed_out_status'] = False
    store['channels'][c_dex]['all_members'][u_dex]['info']['time_out_end'] = - 1

    return


def warn_user(c_dex, u_id):
    '''
        Prompts the bot to send out a tag and also a notification is sent to the user
        that is using expletives. Every 3 warnings, the user is timed out for
        number of warnings * 20 seconds, where they will also be prompted of this
        action by the SEAMS bot.
    '''
    store = data_store.get()

    for u_dex, user in enumerate(store['channels'][c_dex]['all_members']):
        if user['u_id'] == u_id:
            user['info']['warnings'] += 1
            handle = user['handle_str']
            warn_count = user['info']['warnings']
            timeout_len = user['info']['warnings'] * 20
            if user['info']['warnings'] % 3 == 0:
                # bot times them out for x amount of time
                warning_message = format_bot_timeout_warning(
                    handle, timeout_len)
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


'''
clear chat command
'''


def command_clear_chat(channel_id):
    '''
        Clears the chat of the specified channel.
    '''
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            decrement_total_num_messages_in_channel_dm(
                count_not_bot_messages(channel['messages']))
            channel['messages'] = []


def count_not_bot_messages(messages):
    '''
        Counts non bot messages in the channel['messages']
    '''
    counter = 0
    for message in messages:
        if message['message_id'] != - 1:
            counter += 1

    return counter


'''
    voting
'''


def create_poll(c_dex, question, options, c_id):
    '''
        Creates a poll, includes the question, options and is attached to the
        specified channel
    '''
    store = data_store.get()

    if store['channels'][c_dex]['poll']['poll_status']:
        message = "There is already a poll!"
        bot_message = create_bot_message(message)
        store['channels'][c_dex]['messages'].append(bot_message)
        raise InputError(description="There is already an ongoing poll!")

    # Activates the voting dict in the channel
    store['channels'][c_dex]['poll']['poll_status'] = True
    store['channels'][c_dex]['poll']['start_id'] = c_id
    store['channels'][c_dex]['poll']['poll_question'] = question

    for choice in options:
        store['channels'][c_dex]['poll']['poll_info'][choice] = []

    bot_message = create_bot_message(format_bot_poll(c_dex, 0))
    store['channels'][c_dex]['messages'].append(bot_message)


def add_poll_option(c_dex, options):
    '''
        Expand the range of options available for voting
    '''
    store = data_store.get()

    if not store['channels'][c_dex]['poll']['poll_status']:
        message = "There is no ongoing poll!"
        bot_message = create_bot_message(message)
        store['channels'][c_dex]['messages'].append(bot_message)
        raise InputError(description="There is no ongoing poll!")

    for choice in options:
        store['channels'][c_dex]['poll']['poll_info'][choice] = []

    bot_message = create_bot_message(format_bot_poll(c_dex, 0))
    store['channels'][c_dex]['messages'].append(bot_message)


def vote(u_id, c_dex, vote_choice):
    """_summary_
    Allows a user to vote for 1 option only, if you vote for another option
    after you have already voted, your vote will be changed.

    Args:
        u_id (int): _description_
        c_dex (int): _description_
        vote_choice (int): _description_

    Raises:
        InputError: There is no ongoing poll
    """
    store = data_store.get()

    poll_status = store['channels'][c_dex]['poll']['poll_status']

    if poll_status == False:
        warning_message = create_bot_message(format_no_vote())
        store['channels'][c_dex]['messages'].append(warning_message)
        raise InputError(description="There is no ongoing poll!")

    poll_info = store['channels'][c_dex]['poll']['poll_info']

    if has_user_voted(poll_info, u_id):
        for voters in poll_info.items():
            if u_id in voters[1]:
                voters[1].remove(u_id)

            if voters[0] == vote_choice:
                voters[1].append(u_id)
    else:
        for voters in poll_info.items():
            if voters[0] == vote_choice:
                voters[1].append(u_id)

    bot_message = create_bot_message(format_bot_poll(c_dex, 1))
    store['channels'][c_dex]['messages'].append(bot_message)

    return


def end_poll(c_dex, c_id):
    """Cnds the poll in the channel

    Args:
        c_dex (int): _description_
        c_id (int): _description_

    Raises:
        InputError: There is no ongoing poll!
        AccessError: You did not start this poll!
    """
    store = data_store.get()

    poll_info = store['channels'][c_dex]['poll']
    poll_status = poll_info['poll_status']
    poll_started = poll_info['start_id']

    if poll_status == False:
        warning_message = create_bot_message(format_no_vote())
        store['channels'][c_dex]['messages'].append(warning_message)
        raise InputError(description="There is no ongoing poll!")
    elif poll_started != c_id:
        warning_message = create_bot_message(format_no_start())
        store['channels'][c_dex]['messages'].append(warning_message)
        raise AccessError(description="You did not start this poll!")

    results = get_best_poll(poll_info['poll_info'])

    if len(results['most_popular']) == 1:
        result = format_bot_poll(c_dex, 2) + "\n" + \
            f"The most popular choice is {results['return_str']}"
    else:
        result = format_bot_poll(c_dex, 2) + "\n" + \
            f"The most popular choices are tied, they are:{results['return_str']}"

    bot_message = create_bot_message(result)
    store['channels'][c_dex]['messages'].append(bot_message)

    poll_info['poll_info'] = {}
    poll_info['poll_status'] = False
    poll_info['start_id'] = -1


def get_best_poll(poll_info):
    """Returns the poll with the most votes

    Args:
        poll_info (list): _description_

    Returns:
        dict: dict with most popular options and formatted return of the most popular
    """
    largest = 0
    most_popular_options = []
    return_str = ""

    for key in poll_info.items():
        if len(key[1]) > largest:
            largest = len(key[1])
            most_popular_options = [key[0]]
        elif len(key[1]) == largest:
            most_popular_options.append(key[0])

    for option in most_popular_options:
        return_str += "\n" + option

    return {
        'most_popular': most_popular_options,
        'return_str': return_str
    }


def has_user_voted(poll_info, u_id):
    """Checks if a user has voted

    Args:
        poll_info (list): _description_
        u_id (int): _description_

    Returns:
        bool: True if voted, else false
    """
    voted = False
    for voters in poll_info.values():
        if u_id in voters:
            voted = True

    if voted:
        return True
    else:
        return False


'''
    bot message formats
'''


def create_bot_message(warning_message):
    """Formats a bot message

    Args:
        warning_message (str): _description_

    Returns:
        dict: returns a normal message, message id and u_id = - 1 as it is 
        reserved for the bot
    """
    message = {
        'message_id': - 1,
        'u_id': - 1,
        'message': warning_message,
        'time_sent': time_now(),
        'reacts': [],
        'is_pinned': False
    }

    return message


def format_no_start():
    """Formats the message for the bot when the user requesting
    did not start the vode

    Returns:
        str: formatted message for user who did not start vote
    """
    warning_message = "You did not start the vote!"
    return warning_message


def format_bot_warning(warnings, handle):
    """Formats bot message for when a user is warned about swearing

    Args:
        warnings (int): _description_
        handle (str): _description_

    Returns:
        str: formatted string warning user they will be timed out
    """
    warning_message = "Stop swearing @{0}! {1} more warning before timeout!!".format(
        handle, 3 - (warnings % 3))

    return warning_message


def format_bot_timeout_warning(handle, length):
    """Formats a message which will let a user know they will be timed out

    Args:
        handle (str): _description_
        length (int): _description_

    Returns:
        str: formatted message warning user they are timed out
    """
    warning_message = "@{0} has been timed out for {1} seconds for profanity!".format(handle,
                                                                                      length)

    return warning_message


def format_no_vote():
    """Formats a message when a user tries to vote but there is no poll

    Returns:
        str: message instructing user to start poll
    """
    message = "There is no active poll, please do /startpoll <question> <vote1> <vote2> ..."

    return message


def format_bot_poll(c_dex, stage):
    """Formats a message which displays the vote question, options and how many people voted

    Args:
        c_dex (int): _description_
        stage (int): _description_

    Returns:
        str: formatted string which displays poll information
    """
    store = data_store.get()

    poll_stats = store['channels'][c_dex]['poll']
    poll_votes = poll_stats['poll_info']

    vote_len = largest_vote_name(poll_votes)

    if stage == 0:
        poll_message = "A poll has been started\n"
    elif stage == 1:
        poll_message = "Poll in progress...\n"
    else:
        poll_message = "Poll has ended, these were the results\n"

    poll_message += poll_stats['poll_question'] + ":" + "\n"

    for key in poll_votes.items():
        graphics = make_vote_graphics(len(key[1]))
        poll_message += ("\t" + key[0].ljust(vote_len + 5) +
                         graphics + "\n")

    return poll_message


def make_vote_graphics(len):
    """Makes voting graphics, translates number of voters to an emoji

    Args:
        len (int): _description_

    Returns:
        str: str of emojis depending on len
    """
    graphic = "👩 " * len

    return graphic


def largest_vote_name(poll_info):
    """Chooses which option has the largest name for formatting

    Args:
        poll_info (list): _description_

    Returns:
        int: number of letters in the word with option with the largest name
    """
    largest = 0
    for key in poll_info:
        if len(key) > largest:
            largest = len(key)

    return largest


'''
    General helper
'''


def check_command_owner_status(channel_index, auth_user_id):
    """Checks if owner is owner of channel or a global owner

    Args:
        channel_index (int): _description_
        auth_user_id (int): _description_

    Raises:
        AccessError: auth_user_id does not have owner permissions in the channel
    """
    store = data_store.get()

    valid = False
    for owner in store['channels'][channel_index]['owner_members']:
        if owner['u_id'] == auth_user_id or check_global_owner(auth_user_id):
            valid = True

    if valid:
        return
    else:
        raise AccessError(
            'auth_user_id does not have owner permissions in the channel')
