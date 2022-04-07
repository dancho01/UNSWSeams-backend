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

def check_pin_authorised(message_id, u_id, store):
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                if dm['owner']['u_id'] == u_id:
                    return True
                else:
                    raise AccessError(
                        description="user not dm owner")

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if check_channel_owner(channel, u_id):
                    return True
                else:
                    raise AccessError(
                        description="user not channel owner")

    raise InputError(
        description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

def check_if_pinned(message_id, u_id, store): 
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                if message['is_pinned'] == False:
                    message['is_pinned'] = True
                    return
                else:
                    raise InputError(
                        description="Already pinned!")

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if message['is_pinned'] == False:
                    message['is_pinned'] = True
                else:
                    raise InputError(
                        description="Already pinned!")
    return

def check_part_of_message_group(message_id, u_id, store):
    for dm in store['dms']:
        for message in dm['messages']:
            if message_id == message['message_id']:
                member_list = dm_member_list(store, dm['dm_id'])
                if u_id not in member_list:
                    raise InputError(
                            description="Not part of DM")
    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                member_list = channel_member_list(store, channel['channel_id'])
                if u_id not in member_list:
                    user = member_list[0]
                    raise InputError(
                            description=f"Not part of channel {user}")
    return

def channel_member_list(store, channel_id):
    member_list = []
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                member_list.append(member['u_id'])

    return member_list

def dm_member_list(store, dm_id):
    member_list = []
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm['all_members']:
                member_list.append(member['u_id'])

    return member_list