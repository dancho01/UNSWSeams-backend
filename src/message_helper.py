from src.error import AccessError, InputError


def check_valid_message(message_id, u_id, store):
    '''
    checks if message_id refers to a valid message within channel/DM 
    
    Args:
        message_id      int
        u_id            int
        store           copy of datastore
    '''
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                if message['u_id'] == u_id or dm['owner']['u_id'] == u_id:
                    return True
                else:
                    raise AccessError(
                        description="user not dm owner or this message is not written by them")

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if check_channel_owner(channel, u_id) or message['u_id'] == u_id:
                    return True
                else:
                    raise AccessError(
                        description="user not channel owner or this message is not written by them")

    raise InputError(
        description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")


def check_channel_owner(channel, u_id):
    '''
    Checks if user is a owner of the channel
    Returns True if owner
    Returns False if not owner    
    '''
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            return True

    return False


def find_channel_or_dm(store, message_id):
    """
        Returns the message and channel, or message and dm, 
        where the message_id matches the message

    Args:
        store (dict)
        message_id (int)

    Returns:
        c_ret, mess (dict, dict)
    """
    for dm in store['dms']:
        for message in dm['messages']:
            if message_id == message['message_id']:
                c_ret, mess = dm, message

    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                c_ret, mess = channel, message

    return c_ret, mess


def check_if_pinned_v2(message):
    """
       Checks if message is pinned. If unpinned, pins it. If pinned, return InputError 

    Args:
        message (dict)

    Raises:
        InputError
    """
    if message['is_pinned'] == False:
        message['is_pinned'] = True
    else:
        raise InputError(
            description="Already pinned!")


def check_if_unpinned_v2(message):
    """
        Checks if message is unpinned. If pinned, unpins it. If unpinned, return InputError

    Args:
        message (dict)

    Raises:
        InputError
    """

    if message['is_pinned'] == True:
        message['is_pinned'] = False
    else:
        raise InputError(
            description="Already unpinned!")


def check_owner_dm_channel(message_store, u_id, store):
    """
        Checks whether the user is an owner or global owner in a channel.
        Checks if the owner of a dm

    Args:
        message_store (dict)
        u_id (int)
        store (dict)

    Raises:
        AccessError
    """

    if 'owner_members' in message_store.keys():
        for member in message_store['owner_members']:
            if member['u_id'] == u_id:
                return
        for user in store['users']:
            if user['auth_user_id'] == u_id:
                if user['global_permissions'] == 1:
                    return
    else:
        if u_id == message_store['owner']['u_id']:
            return

    raise AccessError(
        description=f"Not owner of channel or DM")
