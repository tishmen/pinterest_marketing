import logging
import random
import traceback

from celery import shared_task
from constance import config

from bot.mailbox import EmailException, MailBox
from bot.models import User
from bot.scripts import (
    CommentScript, ConfirmEmailScript, CreateBoardsScript, CreateUserScript,
    FollowScript, InteractScript, LikeScript, LoginScript, RepinScript,
    SyncScript, UnfollowScript
)
from pinterest_marketing.lock import LockException, lock
from data.models import Board, Comment, Keyword

log = logging.getLogger('pinterest_marketing')


class ResourceException(Exception):

    pass


@shared_task(bind=True, max_retries=1)
def login_task(self, user):
    '''Celery task for loging pinterest user.'''
    try:
        with lock(user.id):
            LoginScript()(user)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def create_user_task(self, user):
    '''Celery task for creating pinterest user.'''
    try:
        with lock(user.id):
            CreateUserScript()(user)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def interact_task(self, user):
    '''Celery task for interacting with pinterest user.'''
    try:
        with lock(user.id):
            InteractScript()(user)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def confirm_email_task(self, user):
    '''Celery task for confirming pinterest user.'''
    try:
        mailbox = MailBox()
        mailbox.login(user.email)
        link = mailbox.get_link()
        with lock(user.id):
            ConfirmEmailScript()(user, link)
    except EmailException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=500)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def create_boards_task(self, user):
    '''Celery task for creating pinterest boards.'''
    try:
        count = random.randint(config.MINIMUM_BOARD, config.MAXIMUM_BOARD)
        boards = Board.random.all()[:count]
        if not boards:
            raise ResourceException(
                'No board resources for {}'.format(self.name)
            )
        with lock(user.id):
            CreateBoardsScript()(user, boards)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def sync_task(self, user):
    '''Celery task for syncing pinterest user with database.'''
    try:
        boards = user.board_set.all()
        with lock(user.id):
            SyncScript()(user, boards)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def repin_task(self, user):
    '''Celery task for repinning random pins.'''
    try:
        board = user.board_set(manager='random').first()
        if not board:
            raise ResourceException(
                'No board resources for {}'.format(self.name)
            )
        keyword = Keyword.random.filter(category=board.category).first()
        if not keyword:
            raise ResourceException(
                'No keyword resources for {}'.format(self.name)
            )
        count = random.randint(config.MINIMUM_REPIN, config.MAXIMUM_REPIN)
        with lock(user.id):
            RepinScript()(user, keyword, board, count)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def like_task(self, user):
    '''Celery task for liking random pins.'''
    try:
        keyword = Keyword.random.first()
        if not keyword:
            raise ResourceException(
                'No keyword resources for {}'.format(self.name)
            )
        count = random.randint(config.MINIMUM_LIKE, config.MAXIMUM_LIKE)
        with lock(user.id):
            LikeScript()(user, keyword, count)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def comment_task(self, user):
    '''Celery task for commenting on random pins.'''
    try:
        keyword = Keyword.random.first()
        if not keyword:
            raise ResourceException(
                'No keyword resources for {}'.format(self.name)
            )
        comments = Comment.random.filter(category=keyword.category).all()
        if not comments:
            raise ResourceException(
                'No comment resources for {}'.format(self.name)
            )
        count = random.randint(config.MINIMUM_COMMENT, config.MAXIMUM_COMMENT)
        with lock(user.id):
            CommentScript()(user, keyword, comments, count)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def follow_task(self, user):
    '''Celery task for following random users.'''
    try:
        keyword = Keyword.random.first()
        if not keyword:
            raise ResourceException(
                'No keyword resources for {}'.format(self.name)
            )
        count = random.randint(config.MINIMUM_FOLLOW, config.MAXIMUM_FOLLOW)
        with lock(user.id):
            FollowScript()(user, keyword, count)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def unfollow_task(self, user):
    '''Celery task for unfollowing random users.'''
    try:
        count = random.randint(
            config.MINIMUM_UNFOLLOW, config.MAXIMUM_UNFOLLOW
        )
        with lock(user.id):
            UnfollowScript()(user, count)
    except LockException:
        log.warn('Retrying %s %d time', self.name, self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def sync_periodic_task(self, user):
    '''Periodic celery task for syncing pinterest users to database.'''
    for user in User.random.all():
        sync_task.delay(user)


@shared_task(bind=True)
def repin_periodic_task(self, user):
    '''Periodic celery task for repining random pins.'''
    for user in User.random.all():
        repin_task.delay(user)


@shared_task(bind=True)
def like_periodic_task(self, user):
    '''Periodic celery task for liking random pins.'''
    for user in User.random.all():
        like_task.delay(user)


@shared_task(bind=True)
def comment_periodic_task(self, user):
    '''Periodic celery task for commenting on random pins.'''
    for user in User.random.all():
        comment_task.delay(user)


@shared_task(bind=True)
def follow_periodic_task(self, user):
    '''Periodic celery task for following random users.'''
    for user in User.random.all():
        follow_task.delay(user)


@shared_task(bind=True)
def unfollow_periodic_task(self, user):
    '''Periodic celery task for unfollowing random users.'''
    for user in User.random.all():
        unfollow_task.delay(user)
