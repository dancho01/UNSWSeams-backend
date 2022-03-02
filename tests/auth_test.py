import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError
from src.other import clear_v1

def test_rego_invalid_fname():
    clear_v1()
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
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchh1ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', '')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston',
                'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')

def test_rego_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail@com', 'winniepooh', 'winston', 'churchhill')
    
def test_rego_invalid_pass():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', '', 'winston', 'churchh!ll')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'pooh', 'winston', 'churchh!ll')
       
    
def test_rego_no_repeats():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')


def test_login_invalid_email():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('wchurchhill@gmail.com', 'winniepooh')
    
def test_login_invalid_pass():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmail.com', 'poohwinnie')

def test_login_invalid_email_format1():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhillgmail.com', 'winniepooh')

def test_login_invalid_email_format2():
    clear_v1()
    auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    with pytest.raises(InputError):
        auth_login_v1('winstonchurchhill@gmailcom', 'winniepooh')

def test_rego_to_login():
    clear_v1()
    rego_id = auth_register_v1('winstonchurchhill@gmail.com', 'winniepooh', 'winston', 'churchhill')
    login_id = auth_login_v1('winstonchurchhill@gmail.com', 'winniepooh')
    assert rego_id == login_id
