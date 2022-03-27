from email import message
from src.error import InputError, AccessError
from src.data_store import check_authorization, data_store, check_user_registered, return_member_information
from src.channel_helper import check_message, time_now, remove_message, member_leave
from src.token import check_valid_token
from src.global_helper import check_valid_channel, check_authorized_user, check_already_auth, check_valid_user, check_owner, check_already_owner
from src.message_helper import generate_new_message_id, check_valid_message
from flask import Response


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

    return_messages = []

    for i in range(start, end_return):
        return_messages.append(
            store['channels'][auth_list_index]['messages'][i])

    return {'messages': return_messages,
            'start': start,
            'end': end
            }


def message_send_v1(token, channel_id, message):
    user_id = check_valid_token(token)['u_id']
    check_message(message)
    channel_index = check_valid_channel(channel_id)
    check_authorized_user(user_id, channel_index)

    new_message_id = generate_new_message_id()
    new_message = {
        'message_id': new_message_id,
        'u_id': user_id,
        'message': message,
        'time_sent': time_now()
    }

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    return {
        'message_id': new_message_id
    }


def messages_edit_v1(token, message_id, message):
    """
    as long as you have a message_id, can find the message in either channels or dms and edit it
    """
    store = data_store.get()
    user_id = check_valid_token(token)['u_id']
    check_message(message)
    check_valid_message(message_id, user_id, store)

    if len(message) == 0:
        messages_remove_v1(token, message_id)

    for channel in store['channels']:
        for messages in channel['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return {}

    for dms in store['dms']:
        for messages in dms['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return {}


def messages_remove_v1(token, message_id):
    user_id = check_valid_token(token)['u_id']
    store = data_store.get()
    check_valid_message(message_id, user_id, store)

    remove_message(message_id)

    return {}


def channel_leave_v1(token, channel_id):
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

    channel_index = check_valid_channel(channel_id)

    check_owner(channel_index, auth_user_id)

    check_already_owner(channel_index, u_id)

    if check_user_registered(u_id, store) == False:
        raise InputError('u_id does not refer to a valid user')

    if check_authorization(u_id, channel_index, store) == False:
        raise InputError(
            'u_id refers to a user who is not a member of the channel')

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
    check_owner(channel_index, auth_user_id)

    if len(store['channels'][channel_index]['owner_members']) == 1: # test if u_id is currently the only owner of the channel
        raise InputError(
            'u_id refers to a user who is currently the only owner of the channel')

    store['channels'][channel_index]['owner_members'].remove(
        return_member_information(u_id, store))

    data_store.set(store)

    return {
    }
