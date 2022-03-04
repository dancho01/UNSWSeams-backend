from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.data_store import check_valid_channel, check_authorization, messages_returned, data_store, check_user_registered


def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users. 
    """
    store = data_store.get()

    # check if auth_user_id exists
    if check_user_registered(auth_user_id, store) == False: 
        raise AccessError("auth_user_id does not exist")

    is_valid_channel = check_valid_channel(channel_id, store)   # returns a tuple (1,index)

    if is_valid_channel:
        # auth_user_id is not a member of the channel
        if check_authorization(auth_user_id, is_valid_channel[1], store): 
            raise AccessError("auth_user_id is not a member of channel")

    # check if channel is valid
    else:
        raise InputError

    # u_id is invalid
    if check_user_registered(u_id, store) == False: 
        raise InputError("u_id does not exist")

    # test if u_id is already a member of the channel
    if check_authorization(u_id, is_valid_channel[1], store): 
        raise InputError("u_id already a member of channel")

    channel_join_v1(u_id, channel_id)
    return {
    }


def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError("auth_user_id passed in is invalid")

    valid_channel = check_valid_channel(channel_id, store)

    if valid_channel == 0:
        raise InputError("channel_id does not refer to a valid channel")
    else:
        channel_index = valid_channel[1]

    if check_authorization(auth_user_id, channel_index, store) == 0:
        raise AccessError(
            "channel_id is valid and the authorized user is not a member of the channel")

    return store['channels'][channel_index]


def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_sent': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError("auth_user_id passed in is invalid")

    found = False
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            found = True
    if found != True:
        raise AccessError("User_id is not valid")

    found = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            found = True
            for member in channel['all_members']:
                if member == auth_user_id:
                    raise InputError(
                        "Authorized user is already a channel member")
            if channel['is_public'] == False:
                raise AccessError(
                    "Cannot join a private channel if not a global owner")

            new_member = auth_user_id
            channel['all_members'].append(new_member)

    if found != True:
        raise InputError("Channel_id does not refer to valid channel")

    data_store.set(store)
    print(store)

    return {
    }


# if __name__ == "__main__":
#     channel_invite_v1(2, 3, 4)