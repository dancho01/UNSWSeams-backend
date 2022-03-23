from email import message
from src.error import InputError, AccessError
from src.data_store import check_authorization, data_store, check_user_registered, return_member_information
from src.channel_helper import check_message, time_now
from src.token import check_valid_token
from src.global_helper import check_valid_channel, check_authorized_user, check_already_auth, check_valid_user, check_owner, check_already_owner
from src.message_helper import generate_new_message_id, check_valid_message
from flask import Response


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


def channel_invite_v1(token, channel_id, u_id):
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

    data_store.set(store)
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

    for i in range(len(store['channels'])):
        for j in range(len(store['channels'][i]['messages'])):
            if store['channels'][i]['messages'][j]['message_id'] == message_id:
                del store['channels'][i]['messages'][j]
                return

    for i in range(len(store['dms'])):
        for j in range(len(store['dms'][i]['messages'])):
            if store['dms'][i]['messages'][j]['message_id'] == message_id:
                del store['dms'][i]['messages'][j]
                return

    data_store.set(store)

    return {}


def channel_leave_v1(token, channel_id):
    user_info = check_valid_token(token)
    # InputError
    channel_index = check_valid_channel(channel_id)
    # AccessError
    check_authorized_user(user_info['u_id'], channel_index)

    store = data_store.get()

    store['channels'][channel_index]['all_members'] = list(filter(
        lambda x: x['u_id'] != user_info['u_id'], store['channels'][channel_index]['all_members']))

    store['channels'][channel_index]['owner_members'] = list(filter(
        lambda x: x['u_id'] != user_info['u_id'], store['channels'][channel_index]['owner_members']))

    data_store.set(store)

    return {}


def channel_join_v1(token, channel_id):

    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    # checks whether user is global owners and stores into permission_id variable
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            permission_id = user['global_permissions']

    channel_index = check_valid_channel(channel_id)
    check_already_auth(auth_user_id, channel_index)

    if store['channels'][channel_index]['is_public'] == False and permission_id != 1:
        # if channel_id is valid and the authorised user is not a member of the channel, AccessError is raised
        raise AccessError(
            'Cannot join a private channel as you are not a global owner')

    store['channels'][channel_index]['all_members'].append(
        return_member_information(auth_user_id, store))

    data_store.set(store)

    return {}


def channel_addowner_v1(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of the channel.
    """
    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    channel_index = check_valid_channel(channel_id)

    # check if token refers to channel owner or has channel owner permissions i.e. is a global owner
    # for user in store['channels'][channel_index]['owner_members']:
    #     if auth_user_id == user['u_id']:
    #         raise AccessError('auth_user_id does not have owner permissions in the channel')
    check_owner(channel_index, auth_user_id)

    check_already_owner(channel_index, auth_user_id)

    # u_id is invalid
    if check_user_registered(u_id, store) == False:
        raise InputError('u_id does not refer to a valid user')

    # test if u_id is a member of the channel
    if check_authorization(u_id, channel_index, store) == False:
        raise InputError(
            'u_id refers to a user who is not a member of the channel')

    # test if u_id is already an owner of the channel
    if u_id in store['channels'][channel_index]['owner_members']:
        raise InputError(
            'u_id refers to a user who is already an owner of the channel')

    store['channels'][channel_index]['owner_members'].append(
        return_member_information(u_id, store))

    data_store.set(store)

    return {
    }


def channel_removeowner_v1(token, channel_id, u_id):
    """
    Remove user with user id u_id as an owner of the channel.
    """
    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    check_valid_user(auth_user_id)
    # returns a tuple (1,index) if channel is valid, else 0
    channel_index = check_valid_channel(channel_id)

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
