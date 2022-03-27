from src.data_store import data_store
from src.token import check_valid_token
from src.global_helper import generate_channel_id, check_valid_user, return_member_information
from src.channels_helper import search_user_channel, return_all_channels, create_new_channel, check_channel_len


def channels_list_v1(token):
    '''
    Provide a list of all channels (and their associated details) that the authorised user is part of.
    '''

    user_data = check_valid_token(token)
    auth_user_id = user_data['u_id']
    check_valid_user(auth_user_id)

    channel_return = search_user_channel(auth_user_id)

    return {'channels': channel_return}


def channels_listall_v1(token):
    '''
    Provide a list of all channels (and their associated details) in Seams.
    '''

    user_data = check_valid_token(token)
    auth_user_id = user_data['u_id']
    check_valid_user(auth_user_id)

    channel_return = return_all_channels()

    return {'channels': channel_return}


def channels_create_v1(token, name, is_public):
    '''
    Creates a new channel with the given name that is either a public or private channel.
    '''
    store = data_store.get()

    user_data = check_valid_token(token)
    auth_user_id = user_data['u_id']
    check_valid_user(auth_user_id)

    # check length of given channel name
    check_channel_len(name)

    # id of new channel is generated based on number of channels
    new_channel_id = generate_channel_id()

    # new dictionary is created to store channel details
    new_channel = create_new_channel(new_channel_id, name, is_public)

    new_channel['owner_members'].append(
        return_member_information(auth_user_id, store))
    new_channel['all_members'].append(
        return_member_information(auth_user_id, store))
    # new_channel is then added to list of channels
    store['channels'].append(new_channel)
    data_store.set(store)

    return {
        'channel_id': new_channel_id,
    }
