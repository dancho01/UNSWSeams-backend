from tkinter.tix import Tree
from src.error import InputError, AccessError
from src.data_store import messages_returned, check_valid_channel, check_authorization, messages_returned, data_store, check_user_registered, return_member_information


def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
        auth_user_id    int         - id of the user that is inviting
        channel_id      int         - id of the channel that the user is inviting u_id to
        u_id            int         - id of the user that is being invited

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is already a member of the channel

    Return Value:
        Returns empty dict as required by spec
    '''
    store = data_store.get()

    # check if auth_user_id is a registered user
    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    # returns a tuple (1,index) if channel is valid, else 0
    channel_status = check_valid_channel(channel_id, store)

    if channel_status == False:
        raise InputError('channel_id does not refer to a valid channel')

    if check_authorization(auth_user_id, channel_status[1], store) == False:
        raise AccessError('auth_user_id is not a member of channel')

    # u_id is invalid
    if check_user_registered(u_id, store) == False:
        raise InputError('u_id passed in is invalid')

    # test if u_id is already a member of the channel
    channel_index = channel_status[1]
    if check_authorization(u_id, channel_index, store) == True:
        raise InputError(
            'u_id refers to a user who is already a member of the channel')

    store['channels'][channel_index]['all_members'].append(
        return_member_information(u_id, store))

    data_store.set(store)

    return {
    }


def channel_details_v1(auth_user_id, channel_id):
    '''
    channel_details_v1 takes the output of check_valid_channel and stores it in channel_status,
    it then ensures that the user is apart of the 'all_users' list within that channel and returns
    all the information for that specified channel at [channel_index].

    Arguments:
        auth_user_id    int         - id of the user that is requesting details
        channel_id      int         - Index of the channel that is to be searched

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel

    Return Value:
        Returns store['channels'][channel_index] if all conditions are satisfied, which contains all the
                information of the channel that is located at channel_index.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    channel_status = check_valid_channel(channel_id, store)

    if channel_status == False:
        raise InputError('channel_id does not refer to a valid channel')
    else:
        channel_index = channel_status[1]

    if check_authorization(auth_user_id, channel_index, store) == False:
        raise AccessError(
            'channel_id is valid and the authorized user is not a member of the channel')

    channel_info = store['channels'][channel_index]

    return {
        "name": channel_info['name'],
        "is_public": channel_info['is_public'],
        "owner_members": channel_info['owner_members'],
        "all_members": channel_info['all_members']
    }


def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    channel_messages_v1 returns a list of dictionaries which contain the keys message_id, u_id, message
    and time_sent, start and end once all error checks are satisfied. End can either be start + 50 if
    there are more messages that can be outputted or -1 if that is the end of all messages within that
    server.

    Iteration 1 note for the tutor:
        Please check assumptions.md

    Arguments:
        auth_user_id    int         - id of the user that is requesting the messages
        channel_id      int         - id of the channel the messages are from
        start           int         - starting index of messages that are to be returned

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when start is greater than the total number of messages in the channel

    Return Value:
        Returns a dictionary with the keys 'messages' which is a list of dictionaries, 'start' which is a integer
                and 'end' which is a int.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    auth_list_index = check_valid_channel(channel_id, store)

    if check_valid_channel(channel_id, store) == False:
        raise InputError('Channel_id does not refer to a valid channel')

    if check_authorization(auth_user_id, auth_list_index[1], store) == False:
        raise AccessError(
            'channel_id is valid and the authorized user is not a member of the channel')

    message_length = len(store['channels'][auth_list_index[1]]['messages'])

    if start > message_length:
        raise InputError(
            'start is greater than the total number of messages in the channel')

    end = start + 50
    if end >= message_length:
        message_return_list = messages_returned(
            auth_list_index[1], start, message_length - 1, store)
        end = -1
    else:
        message_return_list = messages_returned(
            auth_list_index[1], start, end, store)

    return {
        'messages': message_return_list,
        'start': start,
        'end': end,
    }


def channel_join_v1(auth_user_id, channel_id):
    '''
    This function allows the authorized user to join a channel, given the 
    channel_id.

    Arguments:
        auth_user_id    int         - id of the user requesting to join the channel
        channel_id      int         - id of the channel that user wishes to join

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id refers to a channel that is private 
                          and the authorized user is not already a channel member and 
                          is not a global owner 
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when the authorized user is already a member of the channel

    Return Value:
        Return an empty dictionary in all cases
    '''
    store = data_store.get()

    # calls function that checks whether user_id is valid or not
    if check_user_registered(auth_user_id, store) == False:
        raise AccessError(' ')

    # checks whether user is global owners and stores into permission_id variable
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            permission_id = user['global_permissions']

    # calls function that checks if a channel with its given id is valid
    # returns False if not valid, or otherwise, (True, channel_index)
    channel_info = check_valid_channel(channel_id, store)
    if channel_info == False:
        raise InputError('Channel_id does not refer to valid channel')

    # calls function that checks if the user is listed as a member
    channel_id = channel_info[1]
    if check_authorization(auth_user_id, channel_id, store) == True:
        raise InputError('You are already a channel member')

    if store['channels'][channel_id]['is_public'] == False and permission_id != 1:
        # if channel_id is valid and the authorised user is not a member of the channel, AccessError is raised
        raise AccessError(
            'Cannot join a private channel as you are not a global owner')

    store['channels'][channel_id]['all_members'].append(
        return_member_information(auth_user_id, store))

    data_store.set(store)

    return {
    }
