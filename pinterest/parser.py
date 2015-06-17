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

    def get_pins_data(self, json):
        '''Return list of pin data.'''
        data = json['resourceDataCache'][0]['data']
        pins = []
        for result in data:
            if (result['repin_count'] > config.MINIMUM_REPIN_COUNT and
                    result['like_count'] > config.MINIMUM_LIKE_COUNT and
                    result['comment_count'] > config.MINIMUM_COMMENT_COUNT):
                pins.append(
                    {
                        'id': data['id'],
                        'title': data['title'],
                        'description': data['description'],
                        'link': data['link'],
                        'image': data['images']['orig']['url'],
                        'image_signature': data['image_signature'],
                        'repin_count': data['repin_count'],
                        'like_count': data['like_count'],
                        'comment_count': data['comment_count'],
                    }
                )
        return pins

    def get_keyword(self, result, keyword):
        '''Return 'result keyword' if position is 0 else 'keyword result'.'''
        if result['position'] == 0:
            return '{} {}'.format(result['term'], keyword)
        return '{} {}'.format(keyword, result['term'])

    def get_keywords_data(self, json, keyword):
        '''Return list of computed keywords.'''
        data = json['resourceDataCache'][0]['data']['guides']
        keywords = []
        for result in data:
            keywords.append(
                {
                    'keyword': self.get_keyword(result, keyword),
                    'category': keyword.category,
                    'scraped': True,
                }
            )
        return keywords

    def get_pin_repins_url(self, json):
        '''Return pin repins url.'''
        data = json['resourceDataCache'][0]['data']
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
        data = json['resourceDataCache'][0]['data']
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
