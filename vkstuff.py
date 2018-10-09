from initdata import *
import requests

class Factory:

    def __init__(self):
        pass
    
    def find_user(self, id):
        if id.isnumeric():
            return self.get_user_by_id(id)
        else:
            return self.get_user_by_username(id)

    def get_user_by_id(self, id):
        params = {
            'access_token': TOKEN,
            'user_ids': id,
            'fields': 'domain',
            'v': '5.85'
        }
        result = requests.get(API_URL + '/users.get', params)
        json = result.json()
        user = User()
        user.load(json['response'][0])
        user.get_friends()
        user.get_groups()
        return user

    def get_user_by_username(self, username):
        params = {
            'access_token': TOKEN,
            'q': username,
            'fields': 'domain',
            'v': '5.85'
        }
        result = requests.get(API_URL + '/users.search', params)
        json = result.json()

        if 'response' not in json or 'items' not in json['response']:
            print(json)
            raise ValueError('failed search user')

        user = User()
        user.load(json['response']['items'][0])
        user.get_friends()
        user.get_groups()
        return user


class User:

    def __init__(self):
        self.id = None
        self.first_name = ''
        self.last_name = ''
        self.domain = ''
        self.friends = []
        self.groups = []
        self.__is_deactivated = False

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name
    
    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name
    
    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, domain):
        self.__domain = domain

    @property
    def groups(self):
        return self.__groups

    @groups.setter
    def groups(self, groups):
        self.__groups = groups
    
    def __and__(self, other):
        params = {
            'access_token': TOKEN,
            'source_uid': self.id,
            'target_uid': other.id,
            'v': '5.85'
        }
        result = requests.get(API_URL + '/friends.getMutual', params)
        json = result.json()
        common_friends = []
        for friend in self.friends:
            if friend.id in json['response']:
                common_friends.append(friend)

        return common_friends
    
    @property
    def is_deactivated(self):
        return self.__is_deactivated
        
    def __repr__(self):
        return '/'.join((VK_URL, self.domain))

    def __str__(self):
        return '/'.join((VK_URL, self.domain))    

    def show_friends(self):
        for friend in self.friends:
            print(friend)

    def get_friends(self):
        if (self.is_deactivated):
            return False
        
        params = {
            'access_token': TOKEN,
            'user_id': self.id,
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
            print(f'{error_code} {error_msg}')

        for data in items:
            friend = User()
            friend.load(data)
            self.friends.append(friend)

        return True

    def get_groups(self):

        if (self.is_deactivated):
            print('not get groups')
            return []

        params = {
            'access_token': TOKEN,
            'user_id': self.id,
            'extended': 1,
            'fields': 'members_count',
            'v': '5.85'
        }
        result = requests.get(API_URL + '/groups.get', params)
        json = result.json()
        items = []

        if ('response' in json and 'items' in json['response']):
            items = json['response']['items']

        for data in items:
            group = Group()
            if 'id' in data:
                group.id = data['id']
            if 'name' in data:
                group.name = data['name']
            if 'screen_name' in data:
                group.screen_name = data['screen_name']
            if 'members_count' in data:
                group.members_count = data['members_count']

            self.groups.append(group)
        
        return self.groups
        
    def load(self, user_data):
        if type(user_data) == dict:
            for key in user_data:
                if hasattr(self, key):
                    setattr(self, key, user_data[key])
            if ('deactivated' in user_data):
                self.__is_deactivated = True


class Group:
    
    def __init__(self, gid = 0, name = '', screen_name = '', members_count = 0):
        self.gid = gid
        self.name = name
        self.screen_name = screen_name
        self.members_count = 0
    
    @property
    def gid(self):
        return self.__gid

    @gid.setter
    def gid(self, gid):
        self.__gid = gid

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
    
    @property
    def members_count(self):
        return self.__members_count

    @members_count.setter
    def members_count(self, members_count):
        self.__members_count = members_count

    @property
    def screen_name(self):
        return self.__screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        self.__screen_name = screen_name

    def __repr__(self):
        return '/'.join((VK_URL, self.screen_name))

    def __str__(self):
        return '/'.join((VK_URL, self.screen_name))