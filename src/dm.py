from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import check_valid_token
from src.dm_helpers import check_for_duplicates_uids, check_valid_dm, check_user_member_dm, generate_new_dm_id,\
    generate_DM_name, calculate_time_stamp
from src.global_helper import generate_new_message_id, return_member_information, check_valid_user
from src.user_helper import check_for_tags_and_send_notifications, create_channel_invite_notification
from src.iter3_message_helper import is_user_reacted


def dm_create_v1(token, u_ids):
    '''
    Creates a new DM where the members are the creator of this DM and the users
    that it was directed to. The name of the DM is generated based on the users' handles.
    The new DM is added to the list of all DMs

    Args:
        token       str             the encoded JWT string to verify user
        u_ids       list            a list of users the DM is directed to  
    Exceptions:
        InputError      occurs when any u_id in the list does not refer to valid user
        InputError      occurs when there are any duplicate u_ids in the list

    Return:
        Returns a dictionary with the key 'dm_id', the DM's new id           
    '''
    store = data_store.get()

    # checks whether the token is valid and verifies user
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    # InputError raised if any u_id is not valid
    for u_id in u_ids:
        check_valid_user(u_id)

    # InputError raised if any duplicate u_ids exist
    if check_for_duplicates_uids(u_ids) == True:
        raise InputError(description='duplicate user ids not allowed')

    new_dm_id = generate_new_dm_id()
    new_dm_name = generate_DM_name(auth_user_id, u_ids, store)

    new_dm = {'dm_id': new_dm_id,
              'name': new_dm_name,
              'all_members': [],
              'messages': [],
              }

    # adding owner and users to all_members list
    new_dm['all_members'].append(
        return_member_information(auth_user_id, store))
    for u_id in u_ids:
        new_dm['all_members'].append(return_member_information(u_id, store))

    # only original creator of DM is added to owner
    new_dm['owner'] = return_member_information(auth_user_id, store)

    store['dms'].append(new_dm)

    for user_id in u_ids:
        create_channel_invite_notification(-1,
                                           new_dm_id, auth_user_id, user_id, new_dm_name)

    return {
        'dm_id': new_dm_id,
    }


def dm_list_v1(token):
    store = data_store.get()
    '''
    Returns the list of DMs that the user is a member of  
    Args:
        token       str             the encoded JWT string to verify user
    Exceptions:
        None
    Return:
        Returns a list of DMs with the id and name of the name included     
    '''
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    list_dms = []
    for dm in store['dms']:
        for member in dm['all_members']:
            if auth_user_id == member['u_id']:
                list_dms.append({'dm_id': dm['dm_id'], 'name': dm['name']})

    return {
        'dms': list_dms
    }


def dm_remove_v1(token, dm_id):
    '''
    Removes an existing DM, so all members are no longer in the DM. Can only
    be done by the original creator
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        AccessError     occurs when dm_id is valid and the authorised user is not the original DM creator
        AccessError     occurs when dm_id is valid and the authorised user is no longer in the DM
    Return:
        Returns an empty dictionary    
    '''

    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    auth_user_member = return_member_information(auth_user_id, store)

    if auth_user_member not in store['dms'][dm_index]['all_members']:
        raise AccessError(description='user is no longer in the DM')

    if store['dms'][dm_index]['owner']['u_id'] != auth_user_id:
        raise AccessError(description='authorised user is not the DM creator')

    store['dms'] = list(filter(lambda i: i['dm_id'] != dm_id, store['dms']))

    data_store.set(store)

    return {}


def dm_details_v1(token, dm_id):
    '''
    Given a DM with ID dm_id that the authorised user is a member of, provide basic details about the DM.
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        AccessError     dm_id is valid and the authorised user is not a member of the DM
    Return:
        Returns the name of the DM and all the members' info
    '''
    store = data_store.get()

    # checks if token is valid, verifying user
    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    dm_details = store['dms'][dm_index]

    return {
        'name': dm_details['name'],
        'members': dm_details['all_members']
    }


def dm_leave_v1(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM. The creator is 
    allowed to leave and the DM will still exist if this happens. This does not 
    update the name of the DM.
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        AccessError     dm_id is valid and the authorised user is not a member of the DM
    Return:
        Returns an empty dictionary 
    '''
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    store['dms'][dm_index]['all_members'] = list(filter(
        lambda i: i['u_id'] != auth_user_id, store['dms'][dm_index]['all_members']))

    return {}


def dm_messages_v1(token, dm_id, start):
    '''
    Given a DM with ID dm_id that the authorised user is a member of, returns up 
    to 50 messages between index "start" and "start + 50". Message with index 0 
    is the most recent message in the DM. If this function has returned the 
    least recent messages in the DM, returns -1 in "end" to indicate there are no 
    more messages to load after this return.
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
        start       int             the index from which the messages start being returned     
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        InputError      occurs when start is greater than the total number of messages in the channel
        AccessError     dm_id is valid and the authorised user is not a member of the DM
    Return:
        Returns up to a maximum of 50 messages between the start index and the end index    
    '''
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    message_length = len(store['dms'][dm_index]['messages'])

    if start > message_length:
        raise InputError(
            description='start is greater than total number of messages in the DM')

    elif start + 49 <= message_length:
        end_return = end = start + 50
    else:
        end_return = message_length
        end = -1

    return_messages = []

    for i in range(start, end_return):
        return_messages.append(
            store['dms'][dm_index]['messages'][i])

    return_messages.reverse()
    
    list_messages = is_user_reacted(return_messages, auth_user_id)

    return {
        'messages': list_messages,
        'start': start,
        'end': end,
    }


def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id. Every message 
    must have a unique ID.
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
        message     str             the message that the user wishes to send      
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        InputError      occurs when length of message is less than 1 or over 1000 characters
        AccessError     dm_id is valid and the authorised user is not a member of the DM
    Return:
        Returns the newly generated message id 
    '''
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='Message must be between 1 and 1000 characters inclusive')

    check_for_tags_and_send_notifications(message, auth_user_id, -1, dm_id)

    new_message_id = generate_new_message_id()

    new_message = {
        'message_id': new_message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_sent': calculate_time_stamp(),
        'reacts': [],
        'is_pinned' : False
    }

    store['dms'][dm_index]['messages'].append(new_message)

    return {
        'message_id': new_message_id
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from the authorised user to the DM specified by dm_id automatically at a specified time in the future. 
    The returned message_id will only be considered valid for other actions (editing/deleting/reacting/etc) once it has been 
    sent (i.e. after time_sent). If the DM is removed before the message has sent, the message will not be sent. 
    You do not need to consider cases where a user's token is invalidated or a user leaves before the message is scheduled 
    to be sent.
    
    Args:
        token       str             the encoded JWT string to verify user
        dm_id       int             the id of the DM
        message     str             the message that the user wishes to send   
        time_sent   int             the timestamp of the datetime the message is to be sent in the future   
    Exceptions:
        InputError      occurs when dm_id does not refer to a valid DM
        InputError      occurs when length of message is less than 1 or over 1000 characters
        InputError      occurs when time_sent is a time in the past
        AccessError     dm_id is valid and the authorised user is not a member of the DM they are trying to post to
    Return:
        Returns the newly generated message id 
    '''
    store = data_store.get()

    user_info = check_valid_token(token)
    auth_user_id = user_info['u_id']

    if check_valid_dm(dm_id, store) == False:
        raise InputError(description='dm_id does not refer to a valid DM')

    dm_index = check_valid_dm(dm_id, store)[1]

    if check_user_member_dm(auth_user_id, store, dm_index) == False:
        raise AccessError(description='authorised user is not member of DM')

    if len(message) < 1 or len(message) > 1000:
        raise InputError(
            description='Message must be between 1 and 1000 characters inclusive')

    check_for_tags_and_send_notifications(message, auth_user_id, -1, dm_id)

    new_message_id = generate_new_message_id()

    new_message = {
        'message_id': new_message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_sent': calculate_time_stamp()
    }


    time_difference = time_sent - time_now()
    if float(time_difference) < 0:
        raise InputError(
            'time_sent is a time in the past')
    t = threading.Timer(time_difference, store['dms'][dm_index]['messages'].append(new_message))
    t.start()

    return {
        'message_id': new_message_id
    }