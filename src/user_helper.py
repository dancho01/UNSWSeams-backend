import os
import glob
import urllib.request
from PIL import Image
from src.data_store import data_store
from src.error import InputError, AccessError
from src import config


def check_for_tags_and_send_notifications(message, u_id, c_id, dm_id):

    def filter_tags(word):
        if '@' not in word:
            return False
        return True

    sent_message = message
    to_return = []
    message = message.split()

    message = list(filter(lambda t: filter_tags(t), message))

    for word in message:
        if word[0] == '@':
            toProcess = word.split('@')
            if len(toProcess) > 1:
                for word in toProcess:
                    if len(word) > 0:
                        to_return.append(word)
            else:
                word.append(to_return)
        else:
            toProcess = word.split('@')
            if len(toProcess) > 1:
                if len(word) > 0:
                    for i in range(1, len(toProcess)):
                        to_return.append(toProcess[i])

    if len(to_return) > 0:
        for tagged_user in set(to_return):
            print(user_in_channel(tagged_user, c_id, dm_id))
            if user_in_channel(tagged_user, c_id, dm_id):
                notification = create_tag_notification(
                    c_id, dm_id, u_id, sent_message)
                attach_notification(tagged_user, notification)


def create_tag_notification(channel_id, dm_id, tagger_id, message):
    tagger_handle = return_user_handle(tagger_id)
    channel_name = return_channel_or_dm_name(channel_id, dm_id)

    print(message)
    print(type(message))

    notification_message = "{0} tagged you in {1}: {2}".format(
        tagger_handle, channel_name, message[:20])

    notification = {
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': notification_message
    }

    return notification


def create_channel_invite_notification(channel_id, dm_id, inviter_id, invited_id, channel_or_dm_name):
    invited_handle = return_user_handle(invited_id)
    inviter_handle = return_user_handle(inviter_id)
    notification_message = "{0} added you to {1}".format(
        inviter_handle, channel_or_dm_name)

    notification = {
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': notification_message
    }
    attach_notification(invited_handle, notification)


def attach_notification(user_handle, notification):
    store = data_store.get()
    for user in store['users']:
        if user['handle'] == user_handle:
            user['notifications'] = [notification] + user['notifications']


def return_notifications(user_id):

    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == user_id:
            return user['notifications'][:20]


def return_channel_or_dm_name(channel_id, dm_id):
    store = data_store.get()

    if dm_id == -1:
        for channel in store['channels']:
            if channel['channel_id'] == channel_id:
                return channel['name']
    else:
        for dm in store['dms']:
            if dm['dm_id'] == dm_id:
                return dm['name']


def return_user_handle(user_id):
    store = data_store.get()

    for user in store['users']:
        if user['auth_user_id'] == user_id:
            return user['handle']


def user_in_channel(user_handle, channel_id, dm_id):
    store = data_store.get()

    if dm_id == -1:
        for channel in store['channels']:
            if channel['channel_id'] == channel_id:
                for member in channel['all_members']:
                    if member['handle_str'] == user_handle:
                        return True
    else:
        for dm in store['dms']:
            if dm['dm_id'] == dm_id:
                for member in dm['all_members']:
                    if member['handle_str'] == user_handle:
                        return True

    return False

def check_url_status(img_url):
    # try: 
    #     if urllib.request.urlopen(img_url).getcode() != 200:
    #         raise InputError(
    #             description='URL not working!')
    # except: 
    #     raise InputError(
    #             description='URL not working!')
    return

def imgDown(img_url, handle):

    # urllib.request.urlretrieve(img_url, f"image/{handle}.jpg")

    return 

def check_dimensions(x1, y1, x2, y2, handle):
    # imageObject = Image.open(f"image/{handle}.jpg")
    # width, height = imageObject.size
    # if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
    #     raise InputError(
    #         description='Dimensions not in bounds')
    
    # if x1 >= x2 or y1 >= y2:
    #     raise InputError(
    #         description='x1, y1 must be smaller than x2, y2')

    return 

def check_image_type(handle):
    # imageObject = Image.open(f"image/{handle}.jpg")
    # if imageObject.format != 'JPEG':
    #     raise InputError(
    #         description=f'Image must be JPG, should not be {imageObject.format}')
    return 

def crop(x1, y1, x2, y2, handle):
    # imageObject = Image.open(f"image/{handle}.jpg")
    # cropped = imageObject.crop((x1, y1, x2, y2))
    # cropped.save(f"images/{handle}.jpg")

    return
 
def clear_profile_images():
    # removing_files_images = glob.glob('/images/*.jpg')
    # for image in removing_files_images:
    #     os.remove(image)
    
    # removing_files_image = glob.glob('/image/*.jpg')
    # for image in removing_files_image:
    #     os.remove(image)
    # directory = os.getcwd()

    # print(directory)
    directory = os.getcwd()
    for file in os.listdir(f'{directory}/images'):
        os.remove(f'{directory}/images/{file}')
    for file in os.listdir(f'{directory}/image'):
        os.remove(f'{directory}/image/{file}')

    return 