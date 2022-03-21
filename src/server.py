import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.channel import channel_invite_v1, channel_join_v1
from src.error import InputError
from src import config
from src.other import clear_v1
from src.data_store import data_store
from src.persistence import save_data, load_data
from src.auth import auth_register_v1, auth_login_v1


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
    return dumps(result)


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
    data = request.get_json()
    result = auth_register_v1(
        data['email'], data['password'], data['name_first'], data['name_last'])

    save_data()
    return dumps(result)


@APP.route("/clear/v1", methods=['DELETE'])
def clear_flask_v1():
    clear_v1()
    save_data()
    return dumps({})

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
    data = request.get_json()
    result = channel_invite_v1(data['token'], data['channel_id'], data['auth_user_id'])

    save_data()
    return dumps({})

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
    data = request.get_json()
    result = channel_join_v1(data['token'], data['channel_id'])

    save_data()
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner_v1():
    data = request.get_json()
    result = channel_addowner_v1(data['token'], data['channel_id'], data['auth_user_id'])

    save_data()
    return dumps({})

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner_v1():
    data = request.get_json()
    result = channel_removeowner_v1(data['token'], data['channel_id'], data['auth_user_id'])

    save_data()
    return dumps({})

# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=True)  # Do not edit this port
