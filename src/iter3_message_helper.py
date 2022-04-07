
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
