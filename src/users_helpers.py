from src.data_store import data_store


def return_users_information():
    '''
        Return active users' information from data_store
    '''

    store = data_store.get()

    users = []

    for user in store['users']:
        if user['active']:
            users.append({
                'u_id': user['auth_user_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle']
            })

    return users


def return_profile(u_id):
    '''
        Return user's information
    '''
    
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            return {
                'u_id': user['auth_user_id'],
                'email': user['email'],
                'name_last': user['name_last'],
                'name_first': user['name_first'],
                'handle_str': user['handle'],
                'profile_img_url' : user['profile_img_url'],
            }
