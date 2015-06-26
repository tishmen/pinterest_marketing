import random

from constance import config


class Parser(object):

    def get_user_data(self, json):
        '''Return user data.'''
        data = json['resourceDataCache'][0]['data']
        return {
            'board_count': data['board_count'],
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
        }

    def get_pins_data(self, json):
        '''Return pins data.'''
        pins_data = []
        for result in json['resourceDataCache'][0]['data']['results']:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                pins_data.append(
                    {
                        'id': result['id'],
                        'title': result['title'],
                        'description': result['description'],
                        'link': result['link'],
                        'image': result['images']['orig']['url'],
                        'image_signature': result['image_signature'],
                        'repin_count': result['repin_count'],
                        'like_count': result['like_count'],
                        'comment_count': result['comment_count'],
                    }
                )
        return pins_data

    def get_pin_repins_url(self, json):
        '''Return pin repins url.'''
        url = 'https://www.pinterest.com/pin/{}/repins/'
        urls = []
        for result in json['resourceDataCache'][0]['data']['results']:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                urls.append(url.format(result['id']))
        return random.choice(urls)

    def get_pin_urls(self, json):
        '''Return list of pin urls.'''
        url = 'https://www.pinterest.com/pin/{}/'
        urls = []
        for result in json['resourceDataCache'][0]['data']['results']:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                urls.append(url.format(result['id']))
        random.shuffle(urls)
        return urls

    def get_user_urls(self, json):
        '''Return list of user urls.'''
        url = 'https://www.pinterest.com/{}/'
        urls = []
        for result in json['resourceDataCache'][0]['data']:
            if result['pin_count'] > config.MINIMUM_PIN_COUNT:
                urls.append(url.format(result['owner']['username']))
        random.shuffle(urls)
        return urls
