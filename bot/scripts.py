import logging
import random

from selenium.common.exceptions import WebDriverException

from .browser import Browser
from .models import Board
from .parser import Parser
from .selectors import *

log = logging.getLogger('pinterest_marketing')


class LoginScript(Browser):

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

    @staticmethod
    def run(self, user):
        try:
            self.set_up(user)
            self.get_url('https://www.pinterest.com/login/')
            try:
                self.set_email(user.email.address)
                self.set_password(user.password)
                self.click_login()
            except WebDriverException:
                pass
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class CreateUserScript(Browser):

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

    @staticmethod
    def run(self, user):
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
            try:
                self.click_skip()
                self.click_confirm()
            except WebDriverException:
                pass
            self.get_url('http://www.pinterest.com/settings/')
            self.click_country()
            self.click_change_photo()
            self.set_choose_file(user.photo)
            self.set_username(user.username)
            self.set_about(user.about)
            self.set_location(user.location)
            self.click_save_settings()
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class InteractScript(Browser):

    @staticmethod
    def run(self, user):
        try:
            self.set_up(user)
            self.get_url('https://www.pinterest.com/')
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise


class ConfirmScript(Browser):

    @staticmethod
    def run(self, user, url):
        try:
            self.set_up(user)
            self.get_url(url)
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class CreateBoardsScript(Browser):

    def __init__(self):
        self.selectors = CREATE_BOARDS_SELECTORS

    def click_create_board1(self):
        '''Click event on create board1 link.'''
        self.click('create_board1', self.get_element('create_board1'))

    def click_create_board2(self):
        '''Click event on create board2 link.'''
        self.click('create_board2', self.get_element('create_board2'))

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

    def save_board(self, user, board):
        '''Save pinterest board to database.'''
        Board.objects.create(
            user=user,
            name=board.name,
            description=board.description,
            category=board.category,
        )
        log.debug('Saved board %s', board)

    @staticmethod
    def run(self, user, boards):
        try:
            self.set_up(user)
            for board in boards:
                self.get_url(user.url())
                try:
                    self.click_create_board1()
                except WebDriverException:
                    self.click_create_board2()
                self.set_name(board.name)
                self.set_description(board.description)
                self.select_category(board.category)
                self.click_save_board()
                self.save_board(user, board)
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class SyncScript(Browser):

    def __init__(self):
        self.parser = Parser()

    def update_user(self, user, data):
        '''Update user table.'''
        user.__dict__.update(data)
        user.save()
        log.debug('Updated user %s', user)

    def update_board(self, board, data):
        '''Update board table.'''
        board.__dict__.update(data)
        board.save()
        log.debug('Updated board %s', board)

    @staticmethod
    def run(self, user, boards):
        try:
            self.set_up(user)
            self.get_url(user.url())
            self.update_user(user, self.parser.get_user_data(self.get_json()))
            for board in boards:
                self.get_url(board.url())
                self.update_board(
                    board, self.parser.get_board_data(self.get_json())
                )
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class RepinScript(Browser):

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

    @staticmethod
    def run(self, user, keyword, board, count):
        try:
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_pin()
                self.click_board(board.name)
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class LikeScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = LIKE_SELECTORS

    def click_like(self):
        '''Click event on like button.'''
        like = self.get_element('like')
        if like.text == 'Like':
            self.click('like', like)

    @staticmethod
    def run(self, user, keyword, count):
        try:
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_like()
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class CommentScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = COMMENT_SELECTORS

    def set_comment(self, text):
        '''Set comment input to text.'''
        self.send_keys('comment', self.get_element('comment_input'), text)

    def click_comment(self):
        '''Click event on comment button.'''
        self.click('comment', self.get_element('comment_button'))

    @staticmethod
    def run(self, user, keyword, comments, count):
        try:
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.set_comment(random.choice(comments))
                self.click_comment()
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class FollowScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = FOLLOW_SELECTORS

    def click_follow(self):
        '''Click event on follow button.'''
        follow = self.get_element('follow')
        if follow.text == 'Follow':
            self.click('follow', follow)

    @staticmethod
    def run(self, user, keyword, count):
        try:
            self.set_up(user)
            self.get_url(keyword.url())
            self.get_url(self.parser.get_pin_repins_url(self.get_json()))
            for user_url in self.parser.get_user_urls(self.get_json())[:count]:
                self.get_url(user_url)
                self.click_follow()
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)


class UnfollowScript(Browser):

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

    @staticmethod
    def run(self, user, count):
        try:
            self.set_up(user)
            self.get_url(user.following_url())
            self.click_pinners()
            self.click_unfollows(count)
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)
