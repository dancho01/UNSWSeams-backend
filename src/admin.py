from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import check_valid_token
from src.global_helper import check_valid_user, check_global_owner
from src.admin_helper import remove_user_name, remove_user_messages, admin_edit_messages_helper


# use filter


def admin_user_remove_v1(token, u_id):
    auth_user_id = check_valid_token(token)['u_id']
    if check_global_owner(auth_user_id) == False:
        raise AccessError("authorised user is not a global owner")
    check_valid_user(u_id)
    store = data_store.get()
    global_owners = 0
    # check u_id is not the only global owner
    for user in store['users']:
        if check_global_owner(user['auth_user_id']):
            global_owners += 1
        if user['auth_user_id'] == u_id:
            u_profile = user

    if global_owners == 1 and u_profile['global_permissions'] == 1:
        raise InputError(
            "user you are trying to remove is the only global owner")

    remove_user_name(u_id)

    admin_edit_messages_helper(auth_user_id, message_id, "Removed user")

    data_store.set(store)

    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Function: Given a user by their user ID, set their permissions to new permissions described by permission_id.
    Parameters:{ token, u_id, permission_id }
    Return Type:{}
    """
    auth_user_id = check_valid_token(token)['u_id']
    if check_global_owner(auth_user_id) == False:
        raise AccessError('authorised user is not a global owner')
    check_valid_user(u_id)

    if permission_id != 1 and permission_id != 2:
        raise InputError('permission_id is invalid')

    store = data_store.get()
    # check u_id is not the only global owner
    global_owners = 0
    for user in store['users']:
        if check_global_owner(user['auth_user_id']):
            global_owners += 1

    if global_owners == 1:
        if check_global_owner(u_id):
            raise InputError(
                'user you are trying to remove is the only global owner')

    for i in range(len(store['users'])):
        if store['users'][i]['auth_user_id'] == u_id:
            if store['users'][i]['global_permissions'] == permission_id:
                raise InputError(
                    'the user already has the permissions level of permission_id')
            else:
                store['users'][i]['global_permissions'] = permission_id
                data_store.set(store)
                return {}
