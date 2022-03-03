from src.error import InputError, AccessError
from src.data_store import checkValidChannel, checkAuthorization, messagesReturned, data_store


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }


def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    channel_info = checkValidChannel(channel_id, store)

    if channel_info == 0:
        raise InputError("channel_id does not refer to a valid channel")

    channel_index = channel_info[1]

    if checkAuthorization(auth_user_id, channel_index, store) == 0:
        raise AccessError(
            "channel_id is valid and the authorized user is not a member of the channel")

    return store['channels'][channel_index]


def channel_messages_v1(auth_user_id, channel_id, start):

    if start < 0:
        raise InputError(
            "Start is greater than the total number of messages in the channel")

    store = data_store.get()

    if checkValidChannel(channel_id, store) != 0:
        authListIndex = checkValidChannel(channel_id)
    else:
        assert InputError("Channel_id does not refer to a valid channel")

    if checkAuthorization(auth_user_id, authListIndex, store):
        assert AccessError(
            "Channel_id is valid and the authorized user is not a member of the channel")


def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()

    found = False
    for user in store['users']:
        if user['id'] == auth_user_id:
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
                        "Authorised user is already a channel member")
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
