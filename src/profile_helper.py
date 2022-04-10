from ast import In
import re
from src.error import AccessError, InputError
from src.data_store import data_store


def check_name(name_first, name_last):

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(
            description="First name must be between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(
            description="Last name must be between 1 and 50 characters inclusive")

    return


def insert_name(u_id, name_first, name_last):

    store = data_store.get()

    # Updates users information
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last

    # Updates all owners of each channel
    for channels in store['channels']:
        for owner_member in channels['owner_members']:
            if owner_member['u_id'] == u_id:
                owner_member['name_first'] = name_first
                owner_member['name_last'] = name_last

    # Updates owner members
    for channels in store['channels']:
        for all_member in channels['all_members']:
            if all_member['u_id'] == u_id:
                all_member['name_first'] = name_first
                all_member['name_last'] = name_last

    for dm in store['dms']:
        for all_member in dm['all_members']:
            if all_member['u_id'] == u_id:
                all_member['name_first'] = name_first
                all_member['name_last'] = name_last

    data_store.set(store)


def check_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise InputError(description="Invalid email!")

    store = data_store.get()

    for user in store['users']:
        if user['email'] == email:
            raise InputError(
                description="This email is already in use by another user!")


def insert_email(u_id, email):

    store = data_store.get()

    # Updates users information
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['email'] = email

    # Updates all owners of each channel
    for channels in store['channels']:
        for owner_member in channels['owner_members']:
            if owner_member['u_id'] == u_id:
                owner_member['email'] = email
    # Updates owner members
    for channels in store['channels']:
        for all_member in channels['all_members']:
            if all_member['u_id'] == u_id:
                owner_member['email'] = email

    for dm in store['dms']:
        for all_member in dm['all_members']:
            if all_member['u_id'] == u_id:
                owner_member['email'] = email

    data_store.set(store)


def check_handle(handle):

    if len(handle) < 3 or len(handle) > 20:
        raise InputError(
            description="length of handle_str is not between 3 and 20 characters inclusive")

    if not handle.isalnum():
        raise InputError(
            description="handle_str contains characters that are not alphanumeric")

    store = data_store.get()

    for user in store['users']:
        if user['handle'] == handle:
            raise InputError(
                description="the handle is already used by another user")


def insert_handle(u_id, handle):

    store = data_store.get()

    # Updates users information
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            user['handle'] = handle

    # Updates all owners of each channel
    for channels in store['channels']:
        for owner_member in channels['owner_members']:
            if owner_member['u_id'] == u_id:
                owner_member['handle'] = handle
    # Updates owner members
    for channels in store['channels']:
        for all_member in channels['all_members']:
            if all_member['u_id'] == u_id:
                owner_member['handle'] = handle

    for dm in store['dms']:
        for all_member in dm['all_members']:
            if all_member['u_id'] == u_id:
                owner_member['handle'] = handle

    data_store.set(store)
