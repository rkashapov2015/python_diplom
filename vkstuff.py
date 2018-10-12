from initdata import *
import requests


def find_user(id):

    if id.isnumeric():
        return get_user_by_id(id)
    else:
        return get_user_by_username(id)

def get_user_by_username(username):

    params = {
        'access_token': TOKEN,
        'q': username,
        'fields': 'domain',
        'v': '5.85'
    }
    result = requests.get(API_URL + '/users.search', params)
    json = result.json()

    logging.debug(json)
    if 'response' not in json or 'items' not in json['response']:
        logging.error('failed search user')
        raise ValueError(f'failed search user {username}')

    user_data = dict(json['response']['items'][0])
    user_data['friends'] = get_friends(user_data)
    user_data['groups'] = get_groups(user_data)
    return user_data

def get_user_by_id(id):
    params = {
        'access_token': TOKEN,
        'user_ids': id,
        'fields': 'domain',
        'v': '5.85'
    }
    result = requests.get(API_URL + '/users.get', params)
    json = result.json()
    
    user_data = dict(json['response'][0])
    user_data['friends'] = get_friends(user_data)
    user_data['groups'] = get_groups(user_data)
    return user_data

def get_friends(user_data):
    if 'deactivated' in user_data:
        raise ValueError('user not active')
    
    params = {
        'access_token': TOKEN,
        'user_id': user_data['id'],
        'fields': 'domain',
        'v': '5.85'
    }

    result = requests.get(API_URL + '/friends.get', params)
    json = result.json()
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

    params = {
        'access_token': TOKEN,
        'user_id': user_data['id'],
        'extended': 1,
        'fields': 'members_count',
        'v': '5.85'
    }

    result = requests.get(API_URL + '/groups.get', params)
    json = result.json()
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