from vkstuff import *
from urllib.parse import urlencode
import json
import time
import sys
import os


def find_original_groups(user: User):
    groups_id = set(map(lambda group: group.id, user.groups))
    
    count_iterations = len(user.friends)
    print('count friends: ', count_iterations)
    iterator = 0
    
    for friend in user.friends:
        if friend.is_deactivated:
            iterator += 1
            print_process(iterator, count_iterations)
            continue
        groups = get_groups(friend)
        friend.groups = groups
        groups_id_friend = set(map(lambda group: group.id, groups))
        
        groups_id = (groups_id - groups_id_friend)
        
        iterator += 1
        if iterator % 3 == 0:
            time.sleep(1)

        print_process(iterator, count_iterations)

    groups_objects = list(filter(lambda group: group.id in groups_id, user.groups))
    groups_data = []
    
    for group_objects in groups_objects:
        groups_data.append({
            'name': group_objects.name,
            'gid': group_objects.id,
            'members_count': group_objects.members_count
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
        friends = get_friends(user)
        user.friends = friends

        groups = get_groups(user)
        user.groups = groups
        
        print('User: ', user)
        print(len(user.friends))

        groups_data = find_original_groups(user)
        save_to_file('groups.json', groups_data)
    except (KeyboardInterrupt, KeyError, ) as key_error:
        logging.info(key_error)
        exit()
    except ValueError as value_error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error(value_error)
        logging.error(exc_type, fname, exc_tb.tb_lineno)
        exit()
run()