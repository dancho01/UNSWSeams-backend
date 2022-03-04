from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.data_store import checkValidChannel, checkAuthorization, messagesReturned, data_store


def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    
    if checkValidChannel(channel_id, store) == 0:
        raise InputError

    # auth_user_id is not a member of the channel
    auth_channels = channels_list_v1(auth_user_id)["channels"]  # returns a list of channels auth_user is in

    valid_user = False
    # auth_channels is a dictionary of a list of channels
    for channel in auth_channels:
        if channel["channel_id"] == channel_id: 
            valid_user = True
        
        if not valid_user:
            raise AccessError

    # auth_user_id does not exist
    
    found = False 
    for user in store['users']:
        # print(user["id"])
        if user["id"] == auth_user_id:
            found = True 
    if not found:
        raise AccessError() 


    # u_id is invalid, when u_id does not exist
    found = False 
    for user in store['users']:
        if user["id"] == u_id:
            found = True 
    if found != True:
        raise AccessError() 

    """""
    # u_id is already a member of the channel
    user_channels = channels_list_v1(u_id)  # returns a list of channels u_id is in
    if channel_id in user_channels:
        raise InputError
    """""




    checkAuthorization(auth_user_id, index, data_store)     # test if u_id is already a member of the channel

    channel_authorization = data_store['channels'][index]['all_members']
    if auth_user_id in channel_authorization:
        return 1
    else:
        return 0


    channel_join_v1(u_id, channel_id)
    return {
    }


def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    valid_channel = checkValidChannel(channel_id, store)

    if valid_channel == 0:
        raise InputError("channel_id does not refer to a valid channel")
    else:
        channel_index = valid_channel[1]

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


# if __name__ == "__main__":
#     channel_invite_v1(2, 3, 4)