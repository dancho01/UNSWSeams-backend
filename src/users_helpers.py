from src.data_store import data_store


def return_users_information():
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
