from vkstuff import *
from urllib.parse import urlencode
import json
import time
import sys
import os



def find_original_groups(user):    

    groups_id = set(map(lambda group: group['id'], user['groups']))
    count_iterations = len(user['friends'])
    print('count friends: ', count_iterations)
    iterator = 0
    
    for friend in user['friends']:
        if 'deactivated' in friend:
            iterator += 1
            print_process(iterator, count_iterations)
            continue
        
        friend['groups'] = get_groups(friend)
        
        groups_id_friend = set(map(lambda group: group['id'], friend['groups']))
        
        groups_id = (groups_id - groups_id_friend)
        
        iterator += 1
        if iterator % 3 == 0:
            time.sleep(1)

        print_process(iterator, count_iterations)

    groups_objects = list(filter(lambda group: group['id'] in groups_id, user['groups']))
    
    return prepare_groups_for_save(groups_objects)
    
def prepare_groups_for_save(groups_objects):
    groups_data = []
    for group_objects in groups_objects:
        groups_data.append({
            'name': group_objects['name'],
            'gid': group_objects['id'],
            'members_count': group_objects['members_count']
        })
    return groups_data

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def print_process(iterator, total):
    length = 50
    percent = (iterator * 100)/total
    filled_length = int(length * iterator // total)
    print_str =  '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r[' + print_str + ']: %4.2f%%' % percent)
    sys.stdout.flush()
    if iterator == total:
        print()

def run():
    
    oauth_data = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'friends',
        'response_type': 'token'
    }

    if TOKEN == 'NONE':
        full_url = '?'.join((OAUTH_URL, urlencode(oauth_data)))
        print('Получите свой токен')
        print(full_url)
        quit()

    try:
        id = input('Enter id or domain page user: ')
        user = find_user(id)
        
        user['friends'] = get_friends(user)
        user['groups'] = get_groups(user)

        print('User: ', user['domain'])

        groups_data = find_original_groups(user)
        save_to_file('groups.json', groups_data)
    except (KeyboardInterrupt, KeyError, ) as key_error:
        logging.info(key_error)
        exit()
    except ValueError as value_error:
        logging.error(value_error)
        print(value_error)
        exit()
        
run()