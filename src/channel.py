from channels import channels_list_v1, channels_listall_v1
from error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # channel_id is invalid
    all_channels = channels_listall_v1(auth_user_id)
    if channel_id not in all_channels:
        raise InputError

    # auth_user_id is not a member of the channel
    auth_channels = channels_list_v1(auth_user_id)  # returns a list of channels auth_user is in
    if channel_id not in auth_channels:
        raise AccessError

    ###### auth_user_id is invalid, when auth_user_id does not exist
    # not sure how to verify whether a user is valid or not

    ###### u_id is invalid, when u_id does not exist
    # not sure how to verify whether a user is valid or not
    #try: 
    #    user_id = auth_login_v1()

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
