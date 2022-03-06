from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.data_store import check_valid_channel, check_authorization, messages_returned, data_store, check_user_registered


def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users. 

    Arguments:
        auth_user_id    int         - id of the user that is inviting
        channel_id      int         - id of the channel that the user is inviting u_id to
        u_id            int         - id of the user that is being invited 

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is already a member of the channel

    Return Value:
        Returns empty dict as required by spec
    '''
    store = data_store.get()

    # check if auth_user_id is a registered user
    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    # returns a tuple (1,index) if channel is valid else 0
    channel_status = check_valid_channel(channel_id, store)

    if channel_status == False:
        raise InputError('channel_id does not refer to a valid channel')

    if check_authorization(auth_user_id, channel_status[1], store) == False:
        raise AccessError('u_id does not refer to a valid user')

    # u_id is invalid
    if check_user_registered(u_id, store) == False:
        raise InputError('u_id passed in is invalid')

    # test if u_id is already a member of the channel
    channel_id = channel_status[1]
    if check_authorization(u_id, channel_id, store) == True:
        raise InputError(
            'u_id refers to a user who is already a member of the channel')
               
    store['channels'][channel_id]['all_members'].append(u_id)

    return {
    }


def channel_details_v1(auth_user_id, channel_id):
    '''
    channel_details_v1 takes the output of check_valid_channel and stores it in channel_status,
    it then ensures that the user is apart of the 'all_users' list within that channel and returns
    all the information for that specified channel at [channel_index].

    Arguments:
        auth_user_id    int         - id of the user that is requesting details
        channel_id      int         - Index of the channel that is to be searched

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel

    Return Value:
        Returns store['channels'][channel_index] if all conditions are satisfied, which contains all the 
                information of the channel that is located at channel_index.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    channel_status = check_valid_channel(channel_id, store)

    if channel_status == False:
        raise InputError('channel_id does not refer to a valid channel')
    else:
        channel_index = channel_status[1]

    if check_authorization(auth_user_id, channel_index, store) == False:
        raise AccessError(
            'channel_id is valid and the authorized user is not a member of the channel')

    return store['channels'][channel_index]


def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    channel_messages_v1 returns a list of dictionaries which contain the keys message_id, u_id, message
    and time_sent, start and end once all error checks are satisfied. End can either be start + 50 if 
    there are more messages that can be outputted or -1 if that is the end of all messages within that
    server.

    Iteration 1 note for the tutor:
        Please check assumptions.md

    Arguments:
        auth_user_id    int         - id of the user that is requesting the messages
        channel_id      int         - id of the channel the messages are from
        start           int         - starting index of messages that are to be returned

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id is valid and the authorized user is not a member of the channel
        InputError      - Occurs when channel_id does not refer to a valid channel

    Return Value:
        Returns a dictionary with the keys 'messages' which is a list of dictionaries, 'start' which is a integer
                and 'end' which is a int.
    '''
    store = data_store.get()

    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    if start < 0:
        raise InputError(
            'start is greater than the total number of messages in the channel')

    auth_list_index = check_valid_channel(channel_id)
    if auth_list_index == False:
        assert InputError('Channel_id does not refer to a valid channel')

    if check_authorization(auth_user_id, auth_list_index, store) == False:
        assert AccessError(
            'channel_id is valid and the authorized user is not a member of the channel')

    # Function for returning messages will be added here

    # Some pseudocode for next iteration
    # if start + 50 > len (messages) - 1
    #     end = -1

    # This is to check if it has returned all the messages_returned

    # Currently end will only return -1 as there are no messages and messages
    # will return a empty list.

    return {
        'messages': [],
        'start': start,
        'end': - 1,
    }


def channel_join_v1(auth_user_id, channel_id):
    '''
    This function allows the authorised user to join a channel, given the 
    channiel_id.

    Arguments:
        auth_user_id    int         - id of the user requesting to join the channel
        channel_id      int         - id of the channel that user wishes to join

    Exceptions:
        AccessError     - Occurs when auth_user_id passed in is invalid
        AccessError     - Occurs when channel_id refers to a channel that is private 
                          and the authorised user is not already a channel member and 
                          is not a global owner 
        InputError      - Occurs when channel_id does not refer to a valid channel
        InputError      - Occurs when the authorised user is already a member of the channel

    Return Value:
        Return an empty dictionary in all cases
    '''
    store = data_store.get()
    
    # calls function that checks whether user_id is valid or not
    if check_user_registered(auth_user_id, store) == False:
        raise AccessError('auth_user_id passed in is invalid')

    # checks whether user is global owners and stores into permission_id variable
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            permission_id = user['global_permissions']
           
    # calls function that checks if a channel with its given id is valid 
    # returns False if not valid, or otherwise, (True, channel_index)
    channel_info = check_valid_channel(channel_id, store)
    if channel_info == False:
        raise InputError('Channel_id does not refer to valid channel')  
        
    # calls function that checks if the user is listed as a member 
    channel_id = channel_info[1]        
    if check_authorization(auth_user_id, channel_id, store) == True:
        raise InputError('You are already a channel member')

    if store['channels'][channel_id]['is_public'] == False and permission_id != 1:
        # if channel_id is valid and the authorised user is not a member of the channel, AccessError is raised
        raise AccessError('Cannot join a private channel as you are not a global owner')

    store['channels'][channel_id]['all_members'].append(auth_user_id)

    data_store.set(store)

    return {
    }
