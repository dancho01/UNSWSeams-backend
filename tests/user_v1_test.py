import requests
from src import config


'''test for user_profile_v1'''


def test_valid_user():
    '''
    Error raised:
        None
    Explanation:
        User 1's u_id is valid 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params={
                            'token': user1_data['token'], 'u_id': user1_data['auth_user_id']})

    assert response.status_code == 200


def test_invalid_user():
    '''
    Error raised:
        InputError: u_id does not refer to a valid user
    Explanation:
        User 1's u_id is invalid 
    '''
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()

    response = requests.get(config.url + 'user/profile/v1', params={
                            'token': user1_data['token'], 'u_id': user1_data['auth_user_id'] + 1})

    assert response.status_code == 400

'''test for user_profile_upload_v1'''

def test_valid_image():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://cdn.britannica.com/91/181391-050-1DA18304/cat-toes-paw-number-paws-tiger-tabby.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 200

def test_valid_image2():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 200


def test_not_valid_image_jpg():

    requests.delete(config.url + 'clear/v1')

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'Firstt', 'name_last': 'Last'})

    user2_data = user2.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_not_valid_image2_jpg():

    requests.delete(config.url + 'clear/v1')

    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'Firstt', 'name_last': 'Last'})

    user2_data = user2.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user2_data['token'], 'img_url': 'https://www.pngall.com/wp-content/uploads/2016/04/Banana-Free-Download-PNG.png', 'x_start' : 0, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid_dimensions():

    
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : -1, 'y_start': 0, 'x_end' : 100, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid2_dimensions():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : -1, 'y_start': 0, 'x_end' : 1366, 'y_end' : 100})

    assert response.status_code == 400

def test_start_dimension_bigger():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'https://www.billboard.com/wp-content/uploads/2020/05/iu-feb-2020-billboard-1548-1589305869.jpg', 'x_start' : 100, 'y_start': 0, 'x_end' : 4, 'y_end' : 100})

    assert response.status_code == 400

def test_invalid_status_code():

    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'email@gmail.com',
                                                                 'password': 'password', 'name_first': 'First', 'name_last': 'Last'})

    user1_data = user1.json()
    
    response = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
                            'token': user1_data['token'], 'img_url': 'http://localhost:29499/Views/ImageOrgChart/Org_Chart.jpg', 'x_start' : 100, 'y_start': 0, 'x_end' : 4, 'y_end' : 100})

    assert response.status_code == 400
