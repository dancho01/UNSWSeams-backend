import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.channel import channel_invite_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
from src.error import InputError
from src import config
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store
from src.persistence import save_data, load_data
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1, message_senddm_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.channel import message_send_v1, messages_edit_v1, messages_remove_v1, channel_messages_v1
from src.profile import set_name_v1, set_email_v1, set_handle_v1


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


@APP.route("/auth/logout/v1", methods=['DELETE'])
def auth_logout_v1():
    data = request.get_json()
    result = auth_logout(data['token'])

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
    result = channel_invite_v1(data['token'], data['channel_id'], data['u_id'])

    save_data()
    return dumps({})

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
    data = request.get_json()
    result = channel_join_v1(data['token'], data['channel_id'])

    save_data()
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner_v1_wrapper():
    data = request.get_json()
    result = channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])

    save_data()
    return dumps({})
    
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    print(type(channel_id))
    start = int(request.args.get('start'))
    result = channel_messages_v1(
        token, channel_id, start)

    save_data()
    return dumps(result)


@APP.route("/message/send/v1", methods=['POST'])
def messages_send_v1():
    data = request.get_json()
    result = message_send_v1(
        data['token'], data['channel_id'], data['message'])

    save_data()
    store = data_store.get()
    print(store)
    return dumps(result)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2():
    data = request.get_json()
    result = channels_create_v1(data['token'], data['name'], data['is_public'])
    save_data()
    store = data_store.get()
    print(store)
    return dumps(result)


@APP.route("/message/edit/v1", methods=['PUT'])
def messages_edits_v1():
    data = request.get_json()
    result = messages_edit_v1(
        data['token'], data['message_id'], data['message'])

    save_data()
    return dumps(result)


@APP.route("/message/remove/v1", methods=['DELETE'])
def messages_delete_v1():
    data = request.get_json()
    result = messages_remove_v1(data['token'], data['message_id'])

    save_data()
    return dumps(result)


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner_v1_wrapper():
    data = request.get_json()
    result = channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])

    save_data()
    return dumps({})

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list_v2():
    token = request.args.get('token')
    result = channels_list_v1(token)
    return dumps(result)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2():
    token = request.args.get('token')
    result = channels_listall_v1(token)
    return dumps(result)


@APP.route("/user/profile/setname/v1", methods=['PUT'])
def set_name():
    data = request.get_json()
    result = set_name_v1(data['token'], data['name_first'], data['name_last'])
    store = data_store.get()
    print(store)
    return dumps(result)


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def set_email():
    data = request.get_json()
    result = set_email_v1(data['token'], data['email'])
    store = data_store.get()
    print(store)
    return dumps(result)


@ APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def set_handle():
    data = request.get_json()
    result = set_handle_v1(data['token'], data['handle'])
    store = data_store.get()
    print(store)
    return dumps(result)


# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=True)  # Do not edit this port
