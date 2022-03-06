from src.data_store import data_store, check_user_registered
from src.error import InputError, AccessError


def channels_list_v1(auth_user_id):
    '''
    Provide a list of all channels (and their associated details) that the authorised user is part of.

    Arguments:
        auth_user_id    int         - id of the user requesting the channels they are part of and the associated details

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid

    Return Value:
        Returns {channels} if all conditions are satisfied, which a dictionary containing a list
        of dictionaries that contain { channel_id, name }.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    channel_return = []
    for channel in store['channels']:
        if auth_user_id in channel['all_members']:
            channel_return.append(
                {'channel_id': channel['channel_id'], 'name': channel['name']})

    return {'channels': channel_return}


def channels_listall_v1(auth_user_id):
    '''
    Provide a list of all channels (and their associated details) that the authorised user is part of.

    Arguments:
        auth_user_id    int         - id of the user requesting a list of all channels and the associated details

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid

    Return Value:
        Returns {channels} if all conditions are satisfied, which a dictionary containing a list
        of dictionaries that contain { channel_id, name }.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    channel_return = []
    for channel in store['channels']:
        channel_return.append(
            {'channel_id': channel['channel_id'], 'name': channel['name']})

    return {'channels': channel_return}


def channels_create_v1(auth_user_id, name, is_public):
    '''
    This function allows an authorized user to request to make a new channel
    with the given name that is either a public or private channel. The user
    then automatically joins the channel

    Arguments:
        auth_user_id    int         - id of the user that is creating the channel
        name            string      - name of the channel to be created
        is_public       boolean     - variable that indicates whether a channel is public or private

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        InputError      - Occurs when length of name is less than 1 or more than 20 characters

    Return Value:
        Returns a dictionary with the key 'channel_id', which is an integer, if channel is 
        successfully created
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    if len(name) < 1 or len(name) > 20:
        raise InputError('Make sure channel name is no less than 1 character and no more than 20')

    # id of new channel is generated based on number of channels
    new_channel_id = len(store['channels']) + 1

    new_channel = {'channel_id': new_channel_id,
                   'name': name,
                   'is_public': is_public,
                   'owner_members': [auth_user_id],
                   'all_members': [auth_user_id],
                   'messages': [],
                   }
    store['channels'].append(new_channel)
    data_store.set(store)

    return {
        'channel_id': new_channel_id,
    }
