from src.error import AccessError, InputError


def is_user_joined(channel_dm, u_id):
    '''
    Checks to see if a user is a member of a channel/dm
    
    Args:
        channel_dm      dict  
        u_id            int
        
    Return:
        True if user is member
        False if user is not member
    '''
    for member in channel_dm['all_members']:
        if member['u_id'] == u_id:
            return True
    return False


def return_messages_with_query(query_str, channel_dm, query_collection):
    '''
    Returns a collection of messages that contain the query string
    
    Args:
        query_str           string
        channel_dm          dict
        query_collection    list
    
    '''
    for message in channel_dm['messages']:
        if query_str.lower() in message['message'].lower():
            query_collection.append(message)
    return query_collection


def check_invalid_message_id(store, message_id, user_id):
    '''
    checks if message_id is not a valid message within a channel or DM 
    that the authorised user has joined. 
    
    Args:
        store           copy of data structure
        message_id      int
        user_id         int
    
    Raises an InputError if invalid
    
    Returns the message if valid
    '''
    for channel in store['channels']:
        if is_user_joined(channel, user_id):
            result = is_message_id_valid(channel, message_id)
            if result != False:
                return result, 1, channel['channel_id']

    for dm in store['dms']:
        if is_user_joined(dm, user_id):
            result = is_message_id_valid(dm, message_id)
            if result != False:
                return result, 2, dm['dm_id']

    raise InputError(description='message id is not valid')


def is_message_id_valid(channel_dm, message_id):
    '''
    checks to see if message is valid inside a channel/dm
    
    Args:
        channel_dm      dict
        message_id      int
    '''
    for message in channel_dm['messages']:
        if message['message_id'] == message_id:
            return message
    return False


def has_user_already_reacted(message, user_id, react_id):
    '''
    checks if user has already reacted to a message with the given react_id
    
    Args:
        message     dict
        user_id     int
        react_id    int
    '''
    for react in message['reacts']:
        if react['react_id'] == react_id:
            for u_id in react['u_ids']:
                if u_id == user_id:
                    return True
    return False


def add_react_message(user_id, message, react_id):
    '''
    adds a react to the message for the user that just reacted
    
    Args:
        user_id     int
        message     dict
        react_id    int  
    '''
    for react in message['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].append(user_id)
            return

    new_react = generate_new_react(user_id, react_id)

    message['reacts'].append(new_react)


def remove_react_message(user_id, message, react_id):
    '''
    Removes a react from the particular message for the user that just unreacted
    
    Args:
        user_id     int
        message     dict
        react_id    int 
    '''
    for react in message['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'] = list(
                filter(lambda i: i != user_id, react['u_ids']))


def generate_new_react(user_id, react_id):
    '''
    If a user reacts to a message with a new react type, adds a dictionary to the
    list of reacts currently present
    
    Args:
        user_id     int
        react_id    int
    
    Returns:
        returns the new dictionary associated with new react type
    '''
    new_react = {
        'react_id': react_id,
        'u_ids': [],
        'is_this_user_reacted': True
    }
    new_react['u_ids'].append(user_id)

    return new_react


def is_user_reacted(list_messages, auth_id):
    '''
    Modifies the 'is_this_user_reacted' in accordance with whether the authorised
    user has reacted to message
    
    Args:
        list_messages   list
        auth_id         int
        
    Returns:
        returns the updated list
    '''
    for message in list_messages:
        for react in message['reacts']:
            found = False
            for u_id in react['u_ids']:
                if u_id == auth_id:
                    react['is_this_user_reacted'] = True
                    found = True
            if found != True:
                react['is_this_user_reacted'] = False

    return list_messages
