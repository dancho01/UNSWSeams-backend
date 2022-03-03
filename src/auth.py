import re
from src.data_store import data_store
from src.error import InputError

def auth_login_v1(email, password):
    store = data_store.get()
    
    if len(email) < 1:
        raise InputError("Enter an email!")
   
    found = False
    for user in store['users']:
        if user['email'] == email:
            found = True
    if found != True:
        raise InputError("This email is not registered!")
    
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise InputError("Invalid email!")

    if '.' not in email:
        raise InputError("No dot in email!")
    
    if '@' not in email:
        raise InputError("No @ in email!")

    for user in store['users']:
        if user['email'] == email:
            if user['password'] != password:
                raise InputError("Incorrect Password!")
            else:
                return {'auth_user_id': user['id']}

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()
    
    if not name_first.isalpha(): 
         raise InputError("Special characters / numbers are not allowed in the name!")
    
    if not name_last.isalpha():
        raise InputError("Special characters / numbers are not allowed in the name!")
    
    if len(name_first) < 1:
        raise InputError("Input a first name!")
    
    if len(name_first) > 50:
        raise InputError("Input a first name less than or equal to 50 characters!")
    
    if len(name_last) < 1:
        raise InputError("Input a last name!")
    
    if len(name_last) > 50:
        raise InputError("Input a last name less than or equal to 50 characters!")
    
    if '.' not in email:
        raise InputError("No dot in email!")
    
    if '@' not in email:
        raise InputError("No @ in email!")
    
    if len(email) < 1:
        raise InputError("Input an email!")
   
    if len(password) < 6:
        raise InputError("Password must be 6 or more characters!")
    
    for user in store['users']:
        if user['email'] == email:
            raise InputError("This email is already in use by another user!")

    new_id = len(store['users']) + 1
    
 
    new_user = {'id': new_id, 'name': name_first + ' ' + name_last, 'email': email, 'password': password} 
    if new_id == 1:
        new_user['global_permissions'] = 1
    else:
        new_user['global_permissions'] = 2                      
              
    store['users'].append(new_user)

    data_store.set(store)    
    
    return {      
            'auth_user_id': new_id,
    }
    
