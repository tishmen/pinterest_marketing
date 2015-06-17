import random
import logging

from pinterest.models import Pin, Board
from pinterest.browser import Browser
from pinterest.selectors import *
from pinterest.parser import Parser
from store.models import Keyword

log = logging.getLogger('pinterest_marketing')


class LoginScript(Browser):

    '''Login pinterest user script.'''

    def __init__(self):
        self.selectors = LOGIN_SELECTORS

    def set_email(self, text):
        '''Set email input to text.'''
        self.send_keys('email', self.get_element('email'), text)

    def set_password(self, text):
        '''Set password input to text.'''
        self.send_keys('password', self.get_element('password'), text)

    def click_login(self):
        '''Click event on login button.'''
        self.click('login', self.get_element('login'))

    def __call__(self, user):
        '''Run selenium code for LoginScript.'''
        try:
            self.set_up(user)
            self.get_url('https://www.pinterest.com/login/')
            self.set_email(user.email.address)
            self.set_password(user.password)
            self.click_login()
        finally:
            self.destroy(user)


class CreateUserScript(Browser):

    '''Create user on pinterest.'''

    def __init__(self):
        self.selectors = CREATE_USER_SELECTORS

    def set_email(self, text):
        '''Set email input to text.'''
        self.send_keys('email', self.get_element('email'), text)

    def set_password(self, text):
        '''Set password input to text.'''
        self.send_keys('password', self.get_element('password'), text)

    def click_continue(self):
        '''Click event on continue button.'''
        self.click('continue', self.get_element('continue'))

    def set_name(self, text):
        '''Set name input to text.'''
        self.send_keys('name', self.get_element('name'), text)

    def set_age(self, text):
        '''Set age input to text.'''
        self.send_keys('age', self.get_element('age'), text)

    def click_female(self):
        '''Click event on female radio.'''
        self.click('female', self.get_element('female'))

    def click_sign_up(self):
        '''Click event on sign up button.'''
        self.click('sign_up', self.get_element('sign_up'))

    def click_next(self):
        '''Click event on next button.'''
        self.click('next', self.get_element('next'))

    def click_follows(self):
        '''Click event on follows button.'''
        follows = self.get_elements('follows')
        random.shuffle(follows)
        for follow in follows[:random.randint(5, 10)]:
            self.click('follow', follow)

    def click_done(self):
        '''Click event on done button.'''
        self.click('done', self.get_element('done'))

    def click_skip(self):
        '''Click event on skip button.'''
        self.click('skip', self.get_element('skip'))

    def click_confirm(self):
        '''Click event on confirm button.'''
        self.click('confirm', self.get_element('confirm'))

    def click_country(self):
        '''Click event on US country option.'''
        self.click('country', self.get_element('country'))

    def click_change_photo(self):
        '''Click event on change photo button.'''
        self.click('change_photo', self.get_element('change_photo'))

    def set_choose_file(self, text):
        '''Set choose file input to text.'''
        self.send_keys('choose_file', self.get_element('choose_file'), text)

    def set_username(self, text):
        '''Set username input to text.'''
        username = self.get_element('username')
        self.clear('username', username)
        self.send_keys('username', username, text)

    def set_about(self, text):
        '''Set about input to text.'''
        self.send_keys('about', self.get_element('about'), text)

    def set_location(self, text):
        '''Set location input to text.'''
        self.send_keys('location', self.get_element('location'), text)

    def click_save_settings(self):
        '''Click event on save settings button.'''
        self.click('save_settings', self.get_element('save_settings'))

    def __call__(self, user):
        '''Run selenium script for CreateUserScript.'''
        try:
            self.set_up(user)
            self.get_url('http://www.pinterest.com/')
            self.set_email(user.email.address)
            self.set_password(user.password)
            self.click_continue()
            self.set_name(user.name)
            self.set_age(str(user.age))
            self.click_female()
            self.click_sign_up()
            self.click_next()
            self.click_follows()
            self.click_done()
            self.click_skip()
            self.click_confirm()
            self.click_skip()
            self.click_confirm()
            self.get_url('http://www.pinterest.com/settings/')
            self.click_country()
            self.click_change_photo()
            self.set_choose_file(user.photo)
            self.set_username(user.username)
            self.set_about(user.about)
            self.set_location(user.location)
            self.click_save_settings()
        finally:
            self.destroy(user)


class ConfirmEmailScript(Browser):

    '''Confirm email on pinterest.'''

    def __call__(self, user, link):
        '''Run selenium script for ConfirmEmailScript.'''
        try:
            self.set_up(user)
            self.get_url(link)
        finally:
            self.destroy(user)


class CreateBoardsScript(Browser):

    '''Create boards on pinterest.'''

    def __init__(self):
        self.selectors = CREATE_BOARDS_SELECTORS

    def click_create_board(self):
        '''Click event on create board link.'''
        self.click('create_board', self.get_element('create_board'))

    def set_name(self, text):
        '''Set name input to text.'''
        self.send_keys('name', self.get_element('name'), text)

    def set_description(self, text):
        '''Set description input to text.'''
        self.send_keys('description', self.get_element('description'), text)

    def select_category(self, text):
        '''Select category by text.'''
        self.select('category', self.get_element('category'), text)

    def click_save_board(self):
        '''Click event on save board link.'''
        self.click('save_board', self.get_element('save_board'))

    def __call__(self, user, boards):
        '''Run selenium script for CreateBoardsScript.'''
        try:
            self.set_up(user)
            for board in boards:
                self.get_url(user.url())
                self.click_create_board()
                self.set_name(board.spin_name())
                self.set_description(board.spin_description())
                self.select_category(board.category)
                self.click_save_board()
                Board.objects.create(user=user, **board)
        finally:
            self.destroy(user)


class SyncScript(Browser):

    '''Sync user on pinterest to local database.'''

    def __init__(self):
        self.parser = Parser()

    def __call__(self, user, boards):
        '''Run selenium script for SyncUserScript.'''
        try:
            self.set_up(user)
            self.get_url(user.url())
            user.__dict__.update(self.parser.get_user_data(self.get_json()))
            user.save()
            for board in boards:
                self.get_url(board.url())
                board.__dict__.update(
                    self.parser.get_board_data(self.get_json())
                )
                board.save()
        finally:
            self.destroy(user)


class RepinScript(Browser):

    '''Repin random pins on pinterest.'''

    def __init__(self):
        self.parser = Parser()
        self.selectors = REPIN_SELECTORS

    def click_pin(self):
        '''Click event on pin button.'''
        self.click('pin', self.get_element('pin'))

    def click_board(self, board_name):
        '''Click event on board div.'''
        for board in self.get_elements('boards'):
            if board.text.split('\n')[-1] == board_name:
                self.click('board', board)
                break

    def __call__(self, user, keyword, boards, count):
        '''Run selenium script for RepinScript.'''
        try:
            self.set_up(user)
            self.get_url(keyword.search_url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_pin()
                self.click_board(random.choice(boards).name)
        finally:
            self.destroy(user)


class LikeScript(Browser):

    '''Like random pins on pinterest.'''

    def __init__(self):
        self.parser = Parser()
        self.selectors = LIKE_SELECTORS

    def click_like(self):
        '''Click event on like button.'''
        like = self.get_element('like')
        if like.text == 'Like':
            self.click('like', like)

    def __call__(self, user, keyword, count):
        '''Run selenium script for LikeScript.'''
        try:
            self.set_up(user)
            self.get_url(keyword.search_url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_like()
        finally:
            self.destroy(user)


class CommentScript(Browser):

    '''Comment on random pins on pinterest.'''

    def __init__(self):
        self.parser = Parser()
        self.selectors = COMMENT_SELECTORS

    def set_comment(self, text):
        '''Set comment input to text.'''
        self.send_keys('comment', self.get_element('comment_input'), text)

    def click_comment(self):
        '''Click event on comment button.'''
        self.click('comment', self.get_element('comment_button'))

    def __call__(self, user, keyword, comments, count):
        '''Run selenium script for CommentScript.'''
        try:
            self.set_up(user)
            self.get_url(keyword.search_url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.set_comment(random.choice(comments).spin())
                self.click_comment()
        finally:
            self.destroy(user)


class FollowScript(Browser):

    '''Follow random users on pinterest.'''

    def __init__(self):
        self.parser = Parser()
        self.selectors = FOLLOW_SELECTORS

    def click_follow(self):
        '''Click event on follow button.'''
        follow = self.get_element('follow')
        if follow.text == 'Follow':
            self.click('follow', follow)

    def __call__(self, user, keyword, count):
        '''Run selenium script for CommentScript.'''
        try:
            self.set_up(user)
            self.get_url(keyword.search_url())
            self.get_url(self.parser.get_pin_repins_url(self.get_json()))
            for user_url in self.parser.get_user_urls(self.get_json())[:count]:
                self.get_url(user_url)
                self.click_follow()
        finally:
            self.destroy(user)


class UnfollowScript(Browser):

    '''Unfollow random users on pinterest.'''

    def __init__(self):
        self.selectors = UNFOLLOW_SELECTORS

    def click_pinners(self):
        '''Click event on pinners button.'''
        self.click('pinners', self.get_element('pinners'))

    def click_unfollows(self, count):
        '''Click event on unfollow buttons.'''
        for unfollow in self.get_elements('unfollows')[:count]:
            if unfollow.text == 'Unfollow':
                self.click('unfollow', unfollow)

    def __call__(self, user, count):
        '''Run selenium script for UnfollowScript.'''
        try:
            self.set_up(user)
            self.get_url(user.following_url())
            self.click_pinners()
            self.click_unfollows(count)
        finally:
            self.destroy(user)


class ScrapeScript(Browser):

    '''Scrape random pins on pinterest.'''

    def __init__(self):
        self.parser = Parser()

    def __call__(self, user, keyword):
        '''Run selenium script for ScrapeScript.'''
        try:
            self.set_up(user)
            self.get_url(keyword.search_url())
            for pin_data in self.parser.get_pins_data(self.get_json()):
                Pin.objects.update_or_create(keyword=keyword, **pin_data)
        finally:
            self.destroy(user)


class ScrapeKeywordScript(Browser):

    '''Get pinterest keyword suggestions.'''

    def __init__(self):
        self.parser = Parser()

    def __call__(self, user, keywords):
        '''Run selenium script for ScrapeKeywordScript.'''
        try:
            self.set_up(user)
            for keyword in keywords:
                self.get_url(keyword.search_url())
                for keyword_data in self.parser.get_keywords_data(
                        self.get_json(), keyword):
                    Keyword.objects.update_or_create(**keyword_data)
        finally:
            self.destroy(user)
