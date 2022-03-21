from src.error import InputError, AccessError
from src.data_store import check_authorization, messages_returned, data_store, check_user_registered, return_member_information
from src.channel_helper import check_message, time_now
from src.token import check_valid_token
from src.global_helper import check_valid_channel, check_authorized_user, check_already_auth, check_valid_user
from src.message_helper import generate_new_message_id, check_valid_message


def channel_invite_v1(token, channel_id, u_id):
    auth_user_id = check_valid_token(token)['u_id']
    store = data_store.get()

    channel_index = check_valid_channel(channel_id)
    check_valid_user(u_id)
    check_already_auth(auth_user_id, channel_index)
    check_authorized_user(auth_user_id, channel_index)

    store['channels'][channel_index]['all_members'].append(
        return_member_information(u_id, store))

    data_store.set(store)

    return {}


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

    channel_index = check_valid_channel(channel_id)
    check_authorized_user(auth_user_id, channel_index)

    store = data_store.get()

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
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_list_index = check_valid_channel(channel_id)
    check_authorized_user(user_info['u_id'], auth_list_index)

    message_length = len(store['channels'][auth_list_index]['messages'])

    if start > message_length:
        raise InputError(
            'start is greater than the total number of messages in the channel')

    end = start + 50
    if end >= message_length:
        message_return_list = messages_returned(
            auth_list_index, start, message_length - 1, store)
        end = -1
    else:
        message_return_list = messages_returned(
            auth_list_index, start, end, store)

    return {
        'messages': message_return_list,
        'start': start,
        'end': end,
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
        'time': time_now()
    }

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    return {
        'message_id': new_message_id
    }


def messages_edit_v1(token, message_id, message):
    store = data_store.get()
    user_id = check_valid_token(token)['u_id']
    check_message(message)
    check_valid_message(message_id, user_id, store)

    if len(message) == 0:
        messages_remove_v1(token, message_id)

    for channel in store['channels']:
        for messages in channel['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message_id
                messages['time'] = time_now()
                return {}

    for dms in store['dms']:
        for messages in dms['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message_id
                messages['time'] = time_now()
                return {}


def messages_remove_v1(token, message_id):
    user_id = check_valid_token(token)['u_id']
    store = data_store.get()
    check_valid_message(message_id, user_id, store)

    for channel in store['channels']:
        for messages in channel['messages']:
            channel['messages'] = list(
                filter(lambda i: i['message_id'] != message_id, messages))

    for dms in store['dms']:
        for messages in dms['messages']:
            dms['messages'] = list(
                filter(lambda i: i['message_id'] != message_id, messages))

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
    check_authorized_user(auth_user_id, channel_index)

    if store['channels'][channel_id]['is_public'] == False and permission_id != 1:
        # if channel_id is valid and the authorised user is not a member of the channel, AccessError is raised
        raise AccessError(
            'Cannot join a private channel as you are not a global owner')

    store['channels'][channel_id]['all_members'].append(
        return_member_information(auth_user_id, store))

    data_store.set(store)

    return {}
