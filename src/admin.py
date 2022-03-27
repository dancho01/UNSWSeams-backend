from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import check_valid_token
from src.global_helper import check_valid_user, check_global_owner
from src.admin_helper import remove_user_name, remove_user_messages, remove_user_from_channels


def admin_user_remove_v1(token, u_id):
    '''
    Given a user by their u_id, remove them from the Seams. This means they should be removed from all 
    channels/DMs, and will not be included in the list of users returned by users/all. 
    Seams owners can remove other Seams owners (including the original first owner). 
    Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
    Their profile must still be retrievable with user/profile, however name_first should be 'Removed' 
    and name_last should be 'user'. The user's email and handle should be reusable.

    Arguments:
        token           string      - token of the user that is inviting
        u_id            int         - id of the user that is being invited

    Exceptions:
        AccessError     - Occurs when the authorised user is not a global owner
        InputError      - Occurs when u_id does not refer to a valid user
        InputError      - Occurs when u_id refers to a user who is the only global owner

    Return Value:
        Returns empty dict as required by spec
    '''
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

    # Turns their name to Removed user in user database
    remove_user_name(u_id)
    # Turns user name and last name to Removed user in channels
    remove_user_from_channels(u_id)
    # Turns their message to Removed user in all dms and channels
    remove_user_messages(u_id)

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
