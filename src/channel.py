from src.error import InputError, AccessError
from src.data_store import data_store
from src.channel_helper import check_message, remove_message, member_leave, get_messages, edit_message, \
    check_valid_message_or_dm, send_message, create_message, share_message_format, send_dm
from src.token import check_valid_token
from src.global_helper import check_valid_channel, check_authorized_user, check_already_auth, check_valid_user,\
    check_owner, check_already_owner, generate_new_message_id, return_member_information, is_user_member, check_global_owner
from src.message_helper import check_valid_message


def channel_invite_v1(token, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
        token           string      - token of the user that is inviting
        channel_id      int         - id of the channel that the user is inviting u_id to
        u_id            int         - id of the user that is being invited

    Exceptions:
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is already a member of the channel

    Return Value:
        Returns empty dict as required by spec
    '''
    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    channel_index = check_valid_channel(channel_id)
    check_valid_user(u_id)
    check_already_auth(u_id, channel_index)
    check_authorized_user(auth_user_id, channel_index)

    store['channels'][channel_index]['all_members'].append(
        return_member_information(u_id, store))

    data_store.set(store)

    return {}


def channel_details_v1(token, channel_id):
    '''
    Returns the details of a given channel 
    Args: 
        token           str         user's token
        channel_id      int         channel's id
    Returns 
        Returns a dictionary containing { name, is_public, owner_members, all_members } of the channel
    '''

    store = data_store.get()

    user_info = check_valid_token(token)
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_info['u_id'], channel_index)

    channel_info = store['channels'][channel_index]

    return {
        "name": channel_info['name'],
        "is_public": channel_info['is_public'],
        "owner_members": channel_info['owner_members'],
        "all_members": channel_info['all_members']
    }


def channel_messages_v1(token, channel_id, start):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, return up to 50 messages between 
    index "start" and "start + 50". Message with index 0 is the most recent message in the channel. 
    This function returns a new index "end" which is the value of "start + 50", or, if this function has returned 
    the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load 
    after this return.

    Args: 
        token           str         user's token
        channel_id      int         channel's id
        start           int         starting message index
    Returns 
        Returns a dictionary containing { messages, start, end } of the channel. 

    '''
    user_info = check_valid_token(token)
    auth_list_index = check_valid_channel(channel_id)
    check_authorized_user(user_info['u_id'], auth_list_index)

    store = data_store.get()

    message_length = len(store['channels'][auth_list_index]['messages'])

    if start > message_length:
        raise InputError(
            'start is greater than the total number of messages in the channel')
    elif start + 49 <= message_length:
        end_return = end = start + 50
    else:
        end_return = message_length
        end = -1

    return_messages = get_messages(start, end_return, auth_list_index)
    print("RETURNMESSAGES-------------------")
    print(return_messages)

    return {'messages': return_messages,
            'start': start,
            'end': end
            }


def message_send_v1(token, channel_id, message):
    '''
    Send a message from the authorised user to the channel specified by channel_id. 
    Note: Each message should have its own unique ID, i.e. no messages should share an ID with another message, 
    even if that other message is in a different channel.

    Args: 
        token           str         user's token
        channel_id      int         channel's id
        message         str         message to be sent
    Returns 
        Returns a dictionary containing { message_id } of the message. 

    '''
    user_id = check_valid_token(token)['u_id']
    check_message(message)
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)

    new_message_id = generate_new_message_id()

    new_message = create_message(new_message_id, user_id, message)

    send_message(new_message, channel_id)

    return {
        'message_id': new_message_id
    }


def messages_edit_v1(token, message_id, message):
    """
    Given a message, update its text with new text. If the new message is an empty string, the message is deleted.
    As long as you have a message_id, can find the message in either channels or dms and edit it. 
    Args: 
        token           str         user's token
        channel_id      int         channel's id
        message         str         message to be sent
    Returns 
        Returns an empty dictionary {}. 

    """
    if len(message) == 0:
        remove_message(message_id)
        return {}

    store = data_store.get()
    user_id = check_valid_token(token)['u_id']
    check_message(message)
    check_valid_message(message_id, user_id, store)

    edit_message(message_id, message)

    return {}


def messages_remove_v1(token, message_id):
    """
    Given a message_id for a message, this message is removed from the channel/DM

    Args: 
        token           str         user's token
        message_id      int         message's id
    Returns 
        Returns an empty dictionary {}. 

    """
    user_id = check_valid_token(token)['u_id']
    store = data_store.get()
    check_valid_message(message_id, user_id, store)

    remove_message(message_id)

    return {}


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    user_id = check_valid_token(token)['u_id']

    check_message(message)

    to_share = check_valid_message_or_dm(
        og_message_id, channel_id, dm_id, user_id)

    new_message_id = generate_new_message_id()
    format_message_share = share_message_format(to_share, message)
    message_ready = create_message(
        new_message_id, user_id, format_message_share)

    if channel_id == -1:
        send_dm(message_ready, dm_id)
    else:
        send_message(message_ready, channel_id)

    return new_message_id


def channel_leave_v1(token, channel_id):
    """
    Given a channel with ID channel_id that the authorised user is a member of, remove them as a member of the channel. 
    Their messages should remain in the channel. If the only channel owner leaves, the channel will remain.

    Args: 
        token           str         user's token
        channel_id      int         channel's id
    Returns 
        Returns an empty dictionary {}. 

    """
    user_info = check_valid_token(token)
    # InputError
    channel_index = check_valid_channel(channel_id)
    # AccessError
    check_authorized_user(user_info['u_id'], channel_index)

    # Filters that user out of the list of all_members and owner_members
    member_leave(user_info['u_id'], channel_index)

    return {}


def channel_join_v1(token, channel_id):
    '''
    This function allows the authorized user to join a channel, given the 
    channel_id.

    Arguments:
        token           string         - token of the user requesting to join the channel
        channel_id      int         - id of the channel that user wishes to join

    Exceptions:
        AccessError     - Occurs when channel_id refers to a channel that is private 
                          and the authorized user is not already a channel member and 
                          is not a global owner 
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id refers to a user who is already an owner of the channel

    Return Value:
        Return an empty dictionary in all cases
    '''

    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    # checks whether user is global owners and stores into permission_id variable
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            permission_id = user['global_permissions']

    channel_index = check_valid_channel(channel_id)
    check_already_auth(auth_user_id, channel_index)

    if store['channels'][channel_index]['is_public'] == False and permission_id != 1:
        raise AccessError(
            'Cannot join a private channel as you are not a global owner')

    store['channels'][channel_index]['all_members'].append(
        return_member_information(auth_user_id, store))

    data_store.set(store)

    return {}


def channel_addowner_v1(token, channel_id, u_id):
    '''
    This function makes the user with user id u_id an owner of the channel.

    Arguments:
        token           string      - token of the user requesting to join the channel
        channel_id      int         - id of the channel that user wishes to join
        u_id            int         - id of the user that is being made an owner of the channel

    Exceptions:
        AccessError     - Occurs when channel_id is valid and the authorised user does not have owner permissions
                          in the channel 
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is not a member of the channel
        InputError      - Occurs when the authorized user is already an owner of the channel

    Return Value:
        Return an empty dictionary in all cases
    '''

    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()
    print("after data_store.get")
    check_valid_user(u_id)

    channel_index = check_valid_channel(channel_id)

    if check_global_owner(auth_user_id) == False:
        check_owner(channel_index, auth_user_id)

    is_user_member(u_id, channel_index)

    print("before checking owner")
    check_already_owner(channel_index, u_id)

    store['channels'][channel_index]['owner_members'].append(
        return_member_information(u_id, store))

    data_store.set(store)

    return {
    }


def channel_removeowner_v1(token, channel_id, u_id):
    '''
    This function removes the user with user id u_id as an owner of the channel.

    Arguments:
        token           string      - token of the user requesting to join the channel
        channel_id      int         - id of the channel that user wishes to join
        u_id            int         - id of the user that is being made an owner of the channel

    Exceptions:
        AccessError     - Occurs when channel_id is valid and the authorised user does not have owner permissions
                          in the channel 
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is not an owner of the channel
        InputError      - Occurs when the u_id refers to a user who is currently the only owner of the channel

    Return Value:
        Return an empty dictionary in all cases
    '''

    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    check_valid_user(auth_user_id)
    channel_index = check_valid_channel(channel_id)
    if check_global_owner(auth_user_id) == False:
        check_owner(channel_index, auth_user_id)

    # test if u_id is currently the only owner of the channel
    if len(store['channels'][channel_index]['owner_members']) == 1:
        raise InputError(
            'u_id refers to a user who is currently the only owner of the channel')

    store['channels'][channel_index]['owner_members'].remove(
        return_member_information(u_id, store))

    data_store.set(store)

    return {
    }
