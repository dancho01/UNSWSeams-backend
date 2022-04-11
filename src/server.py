import sys
import signal
from json import dumps
from flask import Flask, request,send_from_directory
from flask_cors import CORS
from flask_mail import Mail
from src.channel import channel_invite_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1, message_share_v1, message_sendlater_v1
from src import config
from src.other import clear_v1
from src.data_store import data_store
from src.persistence import save_data, load_data
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1, message_senddm_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout, auth_password_request, auth_password_reset
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.channel import message_send_v1, messages_edit_v1, messages_remove_v1, channel_messages_v1, channel_details_v1, channel_leave_v1, message_pin_v1, message_unpin_v1
from src.set import set_name_v1, set_email_v1, set_handle_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.user import user_profile_v1, notifications_get_v1, user_profile_uploadphoto_v1
from src.users import users_all_v1
from src.message_iter3 import search_v1, message_react_v1, message_unreact_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1


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

APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = 'h09belephant@gmail.com'
APP.config['MAIL_PASSWORD'] = '12345!@#$%'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True
mail = Mail(APP)


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
def auth_register_wrapper():
    data = request.get_json()
    result = auth_register_v1(
        data['email'], data['password'], data['name_first'], data['name_last'])

    save_data()
    return dumps({
        'token': result['token'],
        'auth_user_id': result['auth_user_id']
    })
    
@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_password_request_v1():
    data = request.get_json()
    auth_password_request(mail, data['email']) # passes through the mail object instead of creating a global variable
    save_data()         

    return dumps({})

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_password_reset_v1():
    data = request.get_json()
    auth_password_reset(data['reset_code'], data['new_password'])
    save_data() # por que?       

    return dumps({})



@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_wrapper():
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

    return dumps({
        'messages': result['messages'],
        'start': result['start'],
        'end': result['end']
    })


@APP.route("/message/senddm/v1", methods=['POST'])
def send_message_to_dm():
    info = request.get_json()

    result = message_senddm_v1(
        info['token'], info['dm_id'], info['message'])

    save_data()
    return dumps({
        'message_id': result['message_id']
    })


@APP.route("/message/share/v1", methods=['POST'])
def message_share_wrapper():
    info = request.get_json()

    result = message_share_v1(info['token'], info['og_message_id'], info['message'],
                              info['channel_id'], info['dm_id'])

    save_data()
    return dumps({
        'shared_message_id': result
    })


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_v1():
    data = request.get_json()
    result = auth_logout(data['token'])
    save_data()
    return dumps(result)


@APP.route("/clear/v1", methods=['DELETE'])
def clear_flask_v1():
    result = clear_v1()
    save_data()
    return dumps(result)


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
    data = request.get_json()
    result = channel_invite_v1(data['token'], data['channel_id'], data['u_id'])
    save_data()
    return dumps(result)


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    result = channel_leave_v1(data['token'], data['channel_id'])
    save_data()
    return dumps(result)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
    data = request.get_json()
    result = channel_join_v1(data['token'], data['channel_id'])

    save_data()
    return dumps(result)


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner_v1_wrapper():
    data = request.get_json()
    result = channel_addowner_v1(
        data['token'], data['channel_id'], data['u_id'])
    save_data()
    return dumps(result)


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner_v1_wrapper():
    data = request.get_json()
    result = channel_removeowner_v1(
        data['token'], data['channel_id'], data['u_id'])

    save_data()
    return dumps(result)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    result = channel_messages_v1(token, channel_id, start)
    return dumps(result)


@APP.route("/message/send/v1", methods=['POST'])
def messages_send_v1():
    data = request.get_json()
    result = message_send_v1(
        data['token'], data['channel_id'], data['message'])
    save_data()
    return dumps(result)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2():
    data = request.get_json()
    result = channels_create_v1(data['token'], data['name'], data['is_public'])
    save_data()
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
    save_data()
    return dumps(result)


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def set_email():
    data = request.get_json()
    result = set_email_v1(data['token'], data['email'])
    save_data()
    return dumps(result)


@ APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def set_handle():
    data = request.get_json()
    result = set_handle_v1(data['token'], data['handle_str'])
    save_data()
    return dumps(result)


@APP.route("/user/profile/v1", methods=['GET'])
def get_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    result = user_profile_v1(token, u_id)
    return dumps(result)


@APP.route("/channel/details/v2", methods=['GET'])
def get_channel_details_v2():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    result = channel_details_v1(token, channel_id)
    return dumps(result)


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_v1_wrapper():
    data = request.get_json()
    result = admin_user_remove_v1(data['token'], data['u_id'])
    save_data()
    return dumps(result)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1_wrapper():
    data = request.get_json()
    result = admin_userpermission_change_v1(
        data['token'], data['u_id'], data['permission_id'])
    save_data()
    return dumps(result)


@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    result = users_all_v1(token)
    return dumps(result)


@APP.route("/search/v1", methods=['GET'])
def search_v1_wrapper():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    result = search_v1(token, query_str)
    return dumps(result)


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater_v1_wrapper():
    data = request.get_json()
    result = message_sendlater_v1(
        data['token'], data['channel_id'], data['message'], data['time_sent'])
    save_data()
    return dumps(result)


@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get_wrapper():
    token = request.args.get('token')
    result = notifications_get_v1(token)
    return dumps(result)
    
@APP.route("/message/react/v1", methods=['POST'])    
def message_react_wrapper():
    data = request.get_json()
    result = message_react_v1(data['token'], data['message_id'], data['react_id'])
    save_data()
    return dumps(result)
    
@APP.route("/message/unreact/v1", methods=['POST'])    
def message_unreact_wrapper():
    data = request.get_json()
    result = message_unreact_v1(data['token'], data['message_id'], data['react_id'])
    save_data()
    return dumps(result)   

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()
    result = message_pin_v1(
        data['token'], data['message_id'])
    save_data()
    return dumps(result)

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()
    result = message_unpin_v1(
        data['token'], data['message_id'])
    save_data()
    return dumps(result)

@APP.route("/standup/start/v1", methods=['POST'])
def standup_start_wrapper():
    data = request.get_json()
    result = standup_start_v1(
        data['token'], data['channel_id'], data['length'])

    save_data()
    return dumps(result)


@APP.route("/standup/active/v1", methods=['GET'])
def standup_active_wrapper():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    result = standup_active_v1(token, channel_id)

    return dumps(result)


@APP.route("/standup/send/v1", methods=['POST'])
def standup_send_wrapper():
    data = request.get_json()
    result = standup_send_v1(
        data['token'], data['channel_id'], data['message'])
    save_data()
    return dumps(result)

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def upload_photo():
    data = request.get_json()
    result = user_profile_uploadphoto_v1(
        data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end'])
    save_data()
    return dumps(result)

@APP.route('/images/<path>')
def send_js(path):
    return send_from_directory('../images', path)


# NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    load_data()
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=True)  # Do not edit this port
