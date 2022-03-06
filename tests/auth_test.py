import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError
from src.other import clear_v1


# Tests for auth_register_v1
# Tests if first name is invalid
def test_rego_invalid_fname():
    '''
    Error raised:
        InputError
    Explanation: 
        When first name is not of appropriate length
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', '', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh',
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'churchhill')


# Tests if last name is invalid
def test_rego_invalid_lname():
    '''
    Error raised:
        InputError
    Explanation: 
        When last name is not of appropriate length
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', 'winston', '')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston',
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')


# Tests if email is invalid
def test_rego_invalid_email():
    '''
    Error raised:
        InputError
    Explanation: 
        When email entered is not in a correct format (missing @'s and .'s)
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail@com', 'winniepooh', 'winston', 'churchhill')
    
                         
# Tests if password is invalid  
def test_rego_invalid_pass():
    '''
    Error raised:
        InputError
    Explanation:
        When password entered is less than 6 characters
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         '', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'pooh', 'winston', 'churchh!ll')

# Tests that there are no duplicate emails used
def test_rego_no_repeats():
    '''
    Error raised:
        InputError
    Explanation:
        When another user attempts to use an email that is already being used 
        by someone else
    '''
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com',
                         'winniepooh', 'winston', 'churchhill')

# Tests for auth_login_v1
# Tests that email entered during login is valid
def test_login_invalid_email():
    '''
    Error raised:
        InputError
    Explanation:
        When an email entered does not belong to a user
    ''' 
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('wchurchhill@gmail.com', 'winniepooh')


# Tests that password entered during login is correct
def test_login_invalid_pass():
    '''
    Error raised:
        InputError
    Explanation:
        When password entered does not correspond to the password stored for given email
    '''
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com',
                     'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmail.com', 'poohwinnie')


# Tests that login is successful
def test_rego_to_login():
    '''
    Explanation:
        Tests that the return values of user id is identical upon both register and login
        to ensuure both functions are successful     
    '''
    clear_v1()
    rego_id = auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')['auth_user_id']
    login_id = auth_login_v1('winstonchurchhill@gmail.com', 'winniepooh')['auth_user_id']
    assert rego_id == login_id
