from src.data_store import data_store, check_user_registered
from src.error import InputError, AccessError

def channels_list_v1(auth_user_id):
    store = data_store.get()
    if not check_user_registered(auth_user_id, store): 
        raise AccessError

    auth_channel_list = []

    all_channels = store["channels"]      # channel_id is a list of channels which are dictionaries
    for i in range(len(all_channels)):
        for member in all_channels[i]["all_members"]:
            if member == auth_user_id:
                auth_channel_list.append(all_channels[i])
                break

    return {"channels" : auth_channel_list}

def channels_listall_v1(auth_user_id):
    store = data_store.get()
    if not check_user_registered(auth_user_id, store): 
        raise AccessError
        
    channel_list = []

    channel_id = store["channels"]
    for i in range(len(channel_id)):
        if auth_user_id in channel_id[i]["authorised"]:
            channel_list.append(channel_id[i])

    return {"channels" : channel_list}



def channels_create_v1(auth_user_id, name, is_public):
    store = data_store.get()

    if len(name) < 1:
        raise InputError("Make sure channel name is more than 1 character")

    if len(name) > 20:
        raise InputError(
            "Make sure channel name does not exceed 20 characters")

    found = False
    for user in store["users"]:
        if user["auth_user_id"] == auth_user_id:
            found = True
    if found != True:
        raise AccessError("User_id is not valid")

    new_channel_id = len(store["channels"]) + 1
    new_channel = {"channel_id": new_channel_id,
                   "name": name,
                   "is_public": is_public,
                   "owner_members": [auth_user_id],
                   "all_members": [auth_user_id],
                   }
    store["channels"].append(new_channel)
    data_store.set(store)

    return {
        "channel_id": new_channel_id,
    }

