from src.error import InputError
from src.data_store import data_store


def search_user_channel(u_id):
    '''
        Returns channels that the user is part of 
    '''

    store = data_store.get()
    channel_list = []
    for channel in store['channels']:
        for members in channel['all_members']:
            if u_id == members['u_id']:
                channel_list.append(
                    {'channel_id': channel['channel_id'], 'name': channel['name']})
    return channel_list


def return_all_channels():
    '''
        Returns all channels in Seams
    '''

    store = data_store.get()

    channel_list = []
    for channel in store['channels']:
        channel_list.append(
            {'channel_id': channel['channel_id'], 'name': channel['name']})
    return channel_list


def create_new_channel(new_channel_id, name, is_public):
    '''
        Returns a dictionary which contains channel_id, name, is_public filled in 
    '''

    new_channel = {'channel_id': new_channel_id,
                   'name': name,
                   'is_public': is_public,
                   'owner_members': [],
                   'all_members': [],
                   'messages': [],
                   }
    return new_channel


def check_channel_len(name):
    '''
        Checks channel name length
    '''
    if len(name) < 1 or len(name) > 20:
        raise InputError(
            'Make sure channel name no less than 1 character and no more than 20'
        )
