from initdata import *
import requests


def find_user(id):

    if id.isnumeric():
        return get_user_by_id(id)
    else:
        return get_user_by_username(id)

def get_user_by_username(username):

    json = get_user_from_vk_username(username)

    check_response(json)

    user_data = dict(json['response']['items'][0])
    
    return user_data

def get_user_by_id(id):
    
    json = get_user_from_vk_by_id(id)
    
    check_response(json)

    user_data = dict(json['response'][0])
    return user_data

def get_friends(user_data):

    check_user(user_data)

    json = get_friends_from_vk(user_data['id'])
    items = []
    if ('response' in json and 'items' in json['response']):
        items = json['response']['items']

    if ('error' in json):
        error_code = json['error']['error_code']
        error_msg = json['error']['error_msg']
        logging.error(f'{error_code} {error_msg}')

    friends = []

    for data in items:
        friends.append(data)

    return friends

def get_groups(user_data):
    if 'deactivated' in user_data:
        logging.warning(f'user not active {user_data["id"]}')
        return []

    json = get_groups_from_vk(user_data['id'])
    items = []    
    if ('response' in json and 'items' in json['response']):
        items = json['response']['items']

    if ('error' in json):
        error_code = json['error']['error_code']
        error_msg = json['error']['error_msg']
        logging.warning(f'{error_code} {error_msg}')

    groups = []
    for data in items:
        groups.append(data)

    return groups

def get_user_from_vk_username(username):
    add_params = { 'q': username, 'fields': 'domain' }
    return send_request('users.search', add_params)

def get_user_from_vk_by_id(user_id):
    add_params = { 'user_ids': user_id, 'fields': 'domain' }
    return send_request('users.get', add_params)

def get_friends_from_vk(user_id):
    add_params = { 'user_id': user_id, 'fields': 'domain' }
    return send_request('friends.get', add_params)

def get_groups_from_vk(user_id):
    add_params = { 'user_id': user_id, 'fields': 'members_count', 'extended': 1 }
    return send_request('groups.get', add_params)

def send_request(tail_url, add_params: dict):
    params = { 'access_token': TOKEN, 'v': '5.85' }
    params.update(add_params)
    result = requests.get(API_URL + '/' + tail_url, params)
    return result.json()

def check_user(user_data):
    if 'deactivated' in user_data:
        raise ValueError('user not active')

def check_response(response_data):    
    if 'response' not in response_data or 'items' not in response_data['response']:
        logging.error('response is not valid')
        raise ValueError('response is not valid')
    
    