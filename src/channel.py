from error import InputError, AccessError
import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    
    selectedChannel = data_store.checkValidChannelI(channel_id)
    
    
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
    
    if start < 0:
        raise InputError("Start is greater than the total number of messages in the channel")
    
    if data_store.checkValidChannel(channel_id) != 0:
        authListIndex = data_store.checkValidChannel(channel_id)
    else:
        assert InputError("Channel_id does not refer to a valid channel")
    
    if data_store.checkAuthorization(auth_user_id, authListIndex):
        assert AccessError("Channel_id is valid and the authorized user is not a member of the channel")
    
    end = start + 50
    
    arrayMessages = data_store.messagesReturned(authListIndex, start)  # This function should return array of messages
    
    return {
        
        arrayMessages,
        start,
        end,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
