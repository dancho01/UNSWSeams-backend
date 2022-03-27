from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import check_valid_token
from src.global_helper import check_valid_user, check_global_owner
from src.admin_helper import remove_user_name, remove_user_messages, remove_user_from_channels, only_global_owner_check, remove_from_session_list


# use filter

def admin_user_remove_v1(token, u_id):
    auth_user_id = check_valid_token(token)['u_id']

    # checks to see if this user has global permissions
    if not check_global_owner(auth_user_id):
        raise AccessError("authorised user is not a global owner")

    # checks to see if the user is valid
    check_valid_user(u_id)

    # Checks if this user is the only global owner
    only_global_owner_check(u_id)

    # Turns their name to Removed user in user database
    remove_user_name(u_id)
    # Removes users from all channels
    remove_user_from_channels(u_id)
    # Turns their message to Removed user in all dms and channels
    remove_user_messages(u_id)

    # Removes the user from the session_list
    remove_from_session_list(u_id)
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
