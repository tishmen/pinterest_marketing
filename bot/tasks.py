import logging
import random
import traceback

from celery import Task, shared_task
from constance import config

from data.models import Board, Comment, Keyword
from pinterest_marketing.lock import LockException, lock

from .mailbox import EmailException, MailBox
from .models import User
from .scripts import (
    CommentScript, ConfirmScript, CreateBoardsScript, CreateUserScript,
    FollowScript, InteractScript, LikeScript, LoginScript, RepinScript,
    SyncScript, UnfollowScript
)

log = logging.getLogger('app')


class DataException(Exception):

    pass


class Data(object):

    def get_boards(self):
        '''Return random number of boards or raise DataException.'''
        count = random.randint(config.MINIMUM_BOARD, config.MAXIMUM_BOARD)
        boards = Board.random.all()[:count]
        if not boards:
            raise DataException('No board data for {}'.format(self.name))
        return boards

    def get_board(self, user):
        '''Return random board or raise DataException.'''
        board = user.board_set(manager='random').first()
        if not board:
            raise DataException('No board data for {}'.format(self.name))
        return board

    def get_keyword(self, category):
        '''Return random keyword by category or raise DataException.'''
        keyword = Keyword.random.filter(category=category).first()
        if not keyword:
            raise DataException('No keyword data for {}'.format(self.name))
        return keyword

    def get_comments(self, category):
        '''Return random comments by category or raise DataException.'''
        comments = Comment.random.filter(category=category).all()
        if not comments:
            raise DataException('No comment data for {}'.format(self.name))
        return comments


class LoginTask(Task):

    def run(self, user):
        try:
            with lock(user.id):
                LoginScript.run(user)
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class CreateUserTask(Task):

    def run(self, user):
        try:
            with lock(user.id):
                CreateUserScript.run(user)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class InteractTask(Task):

    def run(self, user):
        try:
            with lock(user.id):
                InteractScript.run(user)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class ConfirmTask(Task):

    def get_link(self, user):
        mailbox = MailBox()
        mailbox.login(user.email)
        return mailbox.get_link()

    def run(self, user):
        try:
            with lock(user.id):
                ConfirmScript.run(user, self.get_link(user))
        except (EmailException, LockException):
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class CreateBoardsTask(Task, Data):

    def run(self, user):
        try:
            with lock(user.id):
                CreateBoardsScript.run(user, self.get_boards())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class SyncTask(Task):

    def get_boards(self, user):
        return user.board_set.all()

    def run(self, user):
        try:
            with lock(user.id):
                SyncScript.run(user, self.get_boards(user))
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class RepinTask(Task, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_REPIN, config.MAXIMUM_REPIN)

    def run(self, user):
        try:
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            with lock(user.id):
                RepinScript.run(user, keyword, board, self.get_count())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class LikeTask(Task, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_LIKE, config.MAXIMUM_LIKE)

    def run(self, user):
        try:
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            with lock(user.id):
                LikeScript.run(user, keyword, self.get_count())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class CommentTask(Task, Data):

    def get_count(self):
            return random.randint(
                config.MINIMUM_COMMENT, config.MAXIMUM_COMMENT
            )

    def run(self, user):
        try:
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            comments = self.get_comments(keyword.category)
            with lock(user.id):
                CommentScript.run(user, keyword, comments, self.get_count())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class FollowTask(Task, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_FOLLOW, config.MAXIMUM_FOLLOW)

    def run(self, user):
        try:
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            with lock(user.id):
                FollowScript.run(user, keyword, self.get_count())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class UnfollowTask(Task):

    def get_count(self):
            return random.randint(
                config.MINIMUM_UNFOLLOW, config.MAXIMUM_UNFOLLOW
            )

    def run(self, user):
        try:
            with lock(user.id):
                UnfollowScript.run(user, self.get_count())
        except LockException:
            log.warn('Retrying %s %d time', self.name, self.request.retries)
            self.retry(countdown=100)
        except Exception:
            log.error('Traceback: %s', traceback.format_exc())
            raise


class PeriodicTask(Task):

    abstract = True

    def get_countdown(self, countdown=0):
        return (
            countdown +
            random.randint(config.MINIMUM_COUNTDOWN, config.MAXIMUM_COUNTDOWN)
        )

    def run(self, task):
        '''Run set of tasks with incrementing countdown.'''
        countdown = self.get_countdown()
        for user in User.random.all():
            countdown = self.get_countdown(countdown)
            task.apply_async((user), countdown=countdown)


@shared_task(bind=True, base=PeriodicTask)
def sync_periodic_task(self):
    self.run(SyncTask())


@shared_task(bind=True, base=PeriodicTask)
def repin_periodic_task(self):
    self.run(RepinTask())


@shared_task(bind=True, base=PeriodicTask)
def like_periodic_task(self):
    self.run(LikeTask())


@shared_task(bind=True, base=PeriodicTask)
def comment_periodic_task(self):
    self.run(CommentTask())


@shared_task(bind=True, base=PeriodicTask)
def follow_periodic_task(self):
    self.run(FollowTask())


@shared_task(bind=True, base=PeriodicTask)
def unfollow_periodic_task(self):
    self.run(UnfollowTask())
