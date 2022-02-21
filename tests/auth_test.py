import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError

# going to turn these tests into just those for auth_register
# will make a new file for auth_login tests

def test_rego_valid():
    assert type(auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')) == dict

def test_rego_invalid_fname():
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'w!nston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winst0n', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', '', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 
                'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'churchhill')
        
def test_rego_invalid_lname():
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchh1ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', '')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston',
                'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')

def test_rego_invalid_pass():
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', '', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'pooh', 'winston', 'churchh!ll')
       
#def test_rego_invalid_email():
#   regex rules
    
def test_rego_no_repeats():
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')


def test_login_invalid_email():
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('wchurchhill@gmail.com', 'winniepooh')
    
def test_login_invalid_pass():
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmail.com', 'poohwinnie')

def test_login_invalid_email_format1():
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhillgmail.com', 'winniepooh')

def test_login_invalid_email_format2():
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmailcom', 'winniepooh')


# invalid email format...
