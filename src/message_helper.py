from src.error import AccessError, InputError
from src.global_helper import check_global_owner

MESSAGE_ID_COUNTER = 0


def generate_new_message_id():
    '''
    Generates a new message_id that is unique and sequentially increases by 1
    Args:
        None
    Return:
        Returns the next message_id
    '''
    global MESSAGE_ID_COUNTER
    MESSAGE_ID_COUNTER += 1
    return MESSAGE_ID_COUNTER


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
                if message['u_id'] == u_id or check_channel_owner(channel, u_id):
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
