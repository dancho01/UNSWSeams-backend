from src.error import AccessError, InputError


def check_valid_message(message_id, u_id, store):

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
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            return True

    return False

def find_channel_or_dm(store, message_id):
    for dm in store['dms']:
        for message in dm['messages']:
            if message_id == message['message_id']:
                c_ret, mess = dm, message

    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                c_ret, mess = channel, message

    return c_ret, message

def check_if_pinned_v2(message):
    if message['is_pinned'] == False:
        message['is_pinned'] = True
    else:
        raise InputError(
            description="Already pinned!")

def check_if_unpinned_v2(message):
    if message['is_pinned'] == True:
        message['is_pinned'] = False
    else:
        raise InputError(
            description="Already unpinned!")

def check_owner_dm_channel(message_store, u_id, store):

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
