
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
    

   
                
                
    
