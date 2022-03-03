from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.data_store import checkValidChannel, checkAuthorization, messagesReturned, data_store



def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    # handle invalid channel_id
    # store["channels"][0]["id"]
    all_channels = channels_listall_v1(auth_user_id)["channels"]
    valid_channel = False
    # all_channels is a dictionary of a list of channels
    for channel in all_channels:
        if channel["channel_id"] == channel_id: 
            valid_channel = True
        
        if not valid_channel:
            raise InputError("invalid channel id")

    # auth_user_id is not a member of the channel
    auth_channels = channels_list_v1(auth_user_id)  # returns a list of channels auth_user is in
    if channel_id not in auth_channels["id"]:
        raise AccessError

    # auth_user_id is invalid, when auth_user_id does not exist
    
    found = False 
    for user in store['users']:
        if user["id"] == auth_user_id:
            found = True 
    if found != True:
        raise AccessError("auth_user_id is invalid") 


    # u_id is invalid, when u_id does not exist
    found = False 
    for user in store['users']:
        if user["id"] == u_id:
            found = True 
    if found != True:
        raise AccessError("u_id is invalid") 


    # u_id is already a member of the channel
    user_channels = channels_list_v1(u_id)  # returns a list of channels u_id is in
    if channel_id in user_channels:
        raise InputError



    channel_join_v1(u_id, channel_id)
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }


# if __name__ == "__main__":
#     channel_invite_v1(2, 3, 4)