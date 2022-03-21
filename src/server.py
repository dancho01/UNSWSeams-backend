import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.data_store import data_store
from src.persistence import save_data, load_data
from src.auth import auth_register_v1, auth_login_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1, message_senddm_v1


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example


@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')

    return dumps({
        'data': data
    })


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
    data = request.get_json()
    result = auth_login_v1(data['email'], data['password'])

    save_data()
    return dumps({
        'token': result['token'],
        'auth_user_id': result['auth_user_id']
    })


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
    data = request.get_json()
    result = auth_register_v1(
        data['email'], data['password'], data['name_first'], data['name_last'])

    save_data()
    return dumps({
        'token': result['token'],
        'auth_user_id': result['auth_user_id']
    })

    
    
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    info = request.get_json()
    result = dm_create_v1(info['token'], info['u_ids'])
    
    save_data()
    return dumps({
        'dm_id': result['dm_id'] 
    })
    
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token')
    result = dm_list_v1(token)
    
    save_data()
    return dumps({
        'dms': result['dms']
    })

@APP.route("/dm/remove/v1", methods=['DELETE'])
def remove_dm():
    info = request.get_json()
    dm_remove_v1(info['token'], info['dm_id'])
    
    save_data()
    return dumps({})
    
    
@APP.route("/dm/details/v1", methods=['GET'])
def get_dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id') 
    
    result = dm_details_v1(token, int(dm_id))
    
    save_data()
    return dumps({
        'name': result['name'],
        'members': result['members']
    })
    
    
@APP.route("/dm/leave/v1", methods=['POST'])
def remove_member_from_dm():
    info = request.get_json()
    dm_leave_v1(info['token'], info['dm_id'])
    
    save_data()
    return dumps({})
    
    
@APP.route("/dm/messages/v1", methods=['GET'])
def return_dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    
    result = dm_messages_v1(token, int(dm_id), int(start))
    
    save_data()
    return dumps({
        'messages': result['messages'],
        'start': result['start'],
        'end': result['end']
    })
    

@APP.route("/message/senddm/v1", methods=['POST'])
def send_message_to_dm():
    info = request.get_json()
    
    result = message_senddm_v1(info['token'], info['dm_id'], info['message'])
    
    save_data()
    return dumps({
        'message_id': result['message_id']
    })
    

@APP.route("/clear/v1", methods=['DELETE'])
def clear_flask_v1():
    clear_v1()

    save_data()

    return dumps({})


# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=True)  # Do not edit this port
