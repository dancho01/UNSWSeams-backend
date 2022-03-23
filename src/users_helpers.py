def return_users_information(store):

    users = []

    for user_index in range(len(store['users'])):
            users.append({
                'u_id': store['users'][user_index]['auth_user_id'],
                'email': store['users'][user_index]['email'],
                'name_first': store['users'][user_index]['name_first'],
                'name_last': store['users'][user_index]['name_last'],
                'handle_str': store['users'][user_index]['handle']
            })
    return users
