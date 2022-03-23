from src.data_store import data_store


def remove_user_name(u_id):

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['name_first'] = "Removed"
            user['name_last'] = "User"

    data_store.set(store)

    return {}


def remove_user_messages(message_id):
    store = data_store.get()

    for i in range(len(store['channels'])):
        for j in range(len(store['channels'][i]['messages'])):
            if store['channels'][i]['messages'][j]['message_id'] == message_id:
                del store['channels'][i]['messages'][j]
                return

    for i in range(len(store['dms'])):
        for j in range(len(store['dms'][i]['messages'])):
            if store['dms'][i]['messages'][j]['message_id'] == message_id:
                del store['dms'][i]['messages'][j]
                return

    data_store.set(store)

    return {}
