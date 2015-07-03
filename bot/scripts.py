import logging
import random

from selenium.common.exceptions import WebDriverException

from .browser import Browser
from .models import Board
from .parser import Parser
from .selectors import *

log = logging.getLogger('app')


class LoginScript(Browser):

    def __init__(self):
        self.selectors = LOGIN_SELECTORS

    def set_email(self, text):
        self.send_keys('email', self.get_element('email'), text)

    def set_password(self, text):
        self.send_keys('password', self.get_element('password'), text)

    def click_login(self):
        self.click('login', self.get_element('login'))

    def run(self, user):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url('https://www.pinterest.com/login/')
            try:
                self.set_email(user.email.address)
                self.set_password(user.password)
                self.click_login()
            except WebDriverException:
                pass


class CreateUserScript(Browser):

    def __init__(self):
        self.selectors = CREATE_USER_SELECTORS

    def set_email(self, text):
        self.send_keys('email', self.get_element('email'), text)

    def set_password(self, text):
        self.send_keys('password', self.get_element('password'), text)

    def click_continue(self):
        self.click('continue', self.get_element('continue'))

    def set_name(self, text):
        self.send_keys('name', self.get_element('name'), text)

    def set_age(self, text):
        self.send_keys('age', self.get_element('age'), text)

    def click_female(self):
        self.click('female', self.get_element('female'))

    def click_sign_up(self):
        self.click('sign_up', self.get_element('sign_up'))

    def click_next(self):
        self.click('next', self.get_element('next'))

    def click_follows(self):
        follows = self.get_elements('follows')
        random.shuffle(follows)
        for follow in follows[:random.randint(5, 10)]:
            self.click('follow', follow)

    def click_done(self):
        self.click('done', self.get_element('done'))

    def click_skip(self):
        self.click('skip', self.get_element('skip'))

    def click_confirm(self):
        self.click('confirm', self.get_element('confirm'))

    def click_country(self):
        self.click('country', self.get_element('country'))

    def click_change_photo(self):
        self.click('change_photo', self.get_element('change_photo'))

    def set_choose_file(self, text):
        self.send_keys('choose_file', self.get_element('choose_file'), text)

    def set_username(self, text):
        username = self.get_element('username')
        self.clear('username', username)
        self.send_keys('username', username, text)

    def set_about(self, text):
        self.send_keys('about', self.get_element('about'), text)

    def set_location(self, text):
        self.send_keys('location', self.get_element('location'), text)

    def click_save_settings(self):
        self.click('save_settings', self.get_element('save_settings'))

    def run(self, user):
        with self.browser_handler(user):
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


class InteractScript(Browser):

    def run(self, user):
        try:
            self.set_up(user)
            self.get_url('https://www.pinterest.com/')
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise


class ConfirmScript(Browser):

    def run(self, user, url):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(url)


class CreateBoardsScript(Browser):

    def __init__(self):
        self.selectors = CREATE_BOARDS_SELECTORS

    def click_create_board1(self):
        self.click('create_board1', self.get_element('create_board1'))

    def click_create_board2(self):
        self.click('create_board2', self.get_element('create_board2'))

    def set_name(self, text):
        self.send_keys('name', self.get_element('name'), text)

    def set_description(self, text):
        self.send_keys('description', self.get_element('description'), text)

    def select_category(self, text):
        self.select('category', self.get_element('category'), text)

    def click_save_board(self):
        self.click('save_board', self.get_element('save_board'))

    def save_board(self, user, board):
        Board.objects.create(
            user=user,
            name=board.name,
            description=board.description,
            category=board.category,
        )
        log.debug('Saved board %s', board)

    def run(self, user, boards):
        with self.browser_handler(user):
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


class SyncScript(Browser):

    def __init__(self):
        self.parser = Parser()

    def update_user(self, user, data):
        user.__dict__.update(data)
        user.save()
        log.debug('Updated user %s', user)

    def update_board(self, board, data):
        board.__dict__.update(data)
        board.save()
        log.debug('Updated board %s', board)

    def run(self, user, boards):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(user.url())
            self.update_user(user, self.parser.get_user_data(self.get_json()))
            for board in boards:
                self.get_url(board.url())
                self.update_board(
                    board, self.parser.get_board_data(self.get_json())
                )


class RepinScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = REPIN_SELECTORS

    def click_pin(self):
        self.click('pin', self.get_element('pin'))

    def click_board(self, board_name):
        for board in self.get_elements('boards'):
            if board.text.split('\n')[-1] == board_name:
                self.click('board', board)
                break

    def run(self, user, keyword, board, count):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_pin()
                self.click_board(board.name)


class LikeScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = LIKE_SELECTORS

    def click_like(self):
        like = self.get_element('like')
        if like.text == 'Like':
            self.click('like', like)

    def run(self, user, keyword, count):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.click_like()


class CommentScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = COMMENT_SELECTORS

    def set_comment(self, text):
        self.send_keys('comment', self.get_element('comment_input'), text)

    def click_comment(self):
        self.click('comment', self.get_element('comment_button'))

    def run(self, user, keyword, comments, count):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(keyword.url())
            for pin_url in self.parser.get_pin_urls(self.get_json())[:count]:
                self.get_url(pin_url)
                self.set_comment(random.choice(comments).comment)
                self.click_comment()


class FollowScript(Browser):

    def __init__(self):
        self.parser = Parser()
        self.selectors = FOLLOW_SELECTORS

    def click_follow(self):
        follow = self.get_element('follow')
        if follow.text == 'Follow':
            self.click('follow', follow)

    def run(self, user, keyword, count):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(keyword.url())
            self.get_url(self.parser.get_pin_repins_url(self.get_json()))
            for user_url in self.parser.get_user_urls(self.get_json())[:count]:
                self.get_url(user_url)
                self.click_follow()


class UnfollowScript(Browser):

    def __init__(self):
        self.selectors = UNFOLLOW_SELECTORS

    def click_pinners(self):
        self.click('pinners', self.get_element('pinners'))

    def click_unfollows(self, count):
        for unfollow in self.get_elements('unfollows')[:count]:
            if unfollow.text == 'Unfollow':
                self.click('unfollow', unfollow)

    def run(self, user, count):
        with self.browser_handler(user):
            self.set_up(user)
            self.get_url(user.following_url())
            self.click_pinners()
            self.click_unfollows(count)
