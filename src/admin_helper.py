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
                store['channels'][i]['messages'][j]['message'] == "Removed user"
                return

    for i in range(len(store['dms'])):
        for j in range(len(store['dms'][i]['messages'])):
            if store['dms'][i]['messages'][j]['message_id'] == message_id:
                store['dms'][i]['messages'][j]['message'] == "Removed user"
                return

    data_store.set(store)

    return {}

def admin_edit_messages_helper(auth_user_id, message_id, message):
    """
    as long as you have a message_id, can find the message in either channels or dms and edit it
    """
    store = data_store.get()
    check_message(message)
    check_valid_message(message_id, auth_user_id, store)

    for channel in store['channels']:
        for messages in channel['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return {}

    for dms in store['dms']:
        for messages in dms['messages']:
            if messages['message_id'] == message_id:
                messages['message'] = message
                return {}
