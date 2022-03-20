
def generate_new_handle(name_first, name_last, store):
    '''
    Generates a unique handle for the recently registered user based on user's first and last name 
    Args:
        name_first      str         user's first name
        name_last       str         user's last name
        store           dict        copy of the data structure in data_store
    Return:
        Returns the final handle that is concatenated such that it is unique    
    '''
    name = name_first + name_last
    handle = ""
    for char in name:
        if char.isalnum():
            handle += char.lower()

    # if concatenated handle is longer than 20 characters, it is cut off at length of 20
    if len(handle) > 20:
        handle = handle[0:20]

    count = 0
    final_handle = handle
    # iterates through list of users to check if handle is already taken
    for user in store['users']:
        if user['handle'] == final_handle:
            final_handle = handle + str(count)
            count += 1

    return final_handle
