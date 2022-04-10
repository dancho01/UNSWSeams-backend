from src.error import AccessError, InputError

def is_user_joined(channel_dm, u_id):
    for member in channel_dm['all_members']:
        if member['u_id'] == u_id:  
            return True
    return False
    
    
def return_messages_with_query(query_str, channel_dm, query_collection):
    for message in channel_dm['messages']:
        if query_str.lower() in message['message'].lower():
            query_collection.append(message)
    return query_collection
    
    
def check_invalid_message_id(store, message_id, user_id):
    for channel in store['channels']:
        if is_user_joined(channel, user_id):
            result = is_message_id_valid(channel, message_id)
            if result != False:            
                return result
      
    for dm in store['dms']:
        if is_user_joined(dm, user_id):
            result = is_message_id_valid(dm, message_id)
            if result != False:
                return result
        
    raise InputError(description='message id is not valid')                  
      
                   
def is_message_id_valid(channel_dm, message_id):
    for message in channel_dm['messages']:
        if message['message_id'] == message_id:
            return message
    return False
    
def has_user_already_reacted(message, user_id, react_id):
    for react in message['reacts']:
        if react['react_id'] == react_id:
            for u_id in react['u_ids']:
                if u_id == user_id:
                    return True
    return False
    
    
def add_react_message(user_id, message, react_id):
    for react in message['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].append = user_id
            return
    
    new_react = generate_new_react(user_id, react_id)
    
    message['reacts'].append(new_react)
    
def remove_react_message(user_id, message, react_id):
    for react in message['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'] = list(filter(lambda i: i != user_id, react['u_ids']))
              
    
def generate_new_react(user_id, react_id):
    new_react = {
        'react_id': react_id,
        'u_ids': [],
        'is_this_user_reacted': True 
    }    
    new_react['u_ids'].append(user_id)
    
    return new_react
