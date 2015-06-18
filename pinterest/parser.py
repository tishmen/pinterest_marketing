import random

from constance import config


class Parser(object):

    '''Parse pinterest json response.'''

    def get_user_data(self, json):
        '''Return user data.'''
        data = json['resourceDataCache'][0]['data']
        return {
            'pin_count': data['pin_count'],
            'like_count': data['like_count'],
            'follower_count': data['follower_count'],
            'following_count': data['following_count'],
        }

    def get_board_data(self, json):
        '''Return board data.'''
        data = json['resourceDataCache'][0]['data']
        return {
            'pin_count': data['pin_count'],
            'follower_count': data['follower_count'],
            'collaborator_count': data['collaborator_count'],
        }

    def get_pin_repins_url(self, json):
        '''Return pin repins url.'''
        data = json['resourceDataCache'][0]['data']['results']
        url = 'https://www.pinterest.com/pin/{}/repins/'
        urls = []
        for result in data:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                urls.append(url.format(result['id']))
        return random.choice(urls)

    def get_pin_urls(self, json):
        '''Return list of pin urls.'''
        data = json['resourceDataCache'][0]['data']['results']
        url = 'https://www.pinterest.com/pin/{}/'
        urls = []
        for result in data:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                urls.append(url.format(result['id']))
        random.shuffle(urls)
        return urls

    def get_user_urls(self, json):
        '''Return list of user urls.'''
        data = json['resourceDataCache'][0]['data']
        url = 'https://www.pinterest.com/{}/'
        urls = []
        for result in data:
            if result['pin_count'] > config.MINIMUM_PIN_COUNT:
                urls.append(url.format(result['owner']['username']))
        random.shuffle(urls)
        return urls
