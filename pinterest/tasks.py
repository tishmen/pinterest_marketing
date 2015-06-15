import logging
import traceback
import random

from celery import shared_task
from constance import config

from pinterest.scripts import (
    CreateUserScript, LoginScript, CreateBoardsScript, RepinScript, LikeScript,
    CommentScript, FollowScript, UnfollowScript
)
from store.models import Keyword, Comment, Board
from pinterest_marketing.lock import lock, LockException

log = logging.getLogger('pinterest_marketing')


@shared_task(bind=True)
def create_user_task(self, user):
    '''Celery task for creating pinterest user.'''
    try:
        with lock(user.id):
            CreateUserScript()(user)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def login_task(self, user):
    '''Celery task for loging pinterest user.'''
    try:
        with lock(user.id):
            LoginScript()(user)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def create_boards_task(self, user):
    '''Celery task for creating pinterest boards.'''
    try:
        count = random.randint(config.MINIMUM_BOARD, config.MAXIMUM_BOARD)
        boards = Board.random.all()[:count]
        with lock(user.id):
            CreateBoardsScript()(user, boards)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def repin_task(self, user):
    '''Celery task for repinning random pin.'''
    try:
        keyword = Keyword.random.first()
        boards = user.board_set.filter(category=keyword.category).all()
        count = random.randint(config.MINIMUM_REPIN, config.MAXIMUM_REPIN)
        with lock(user.id):
            RepinScript()(user, keyword, boards, count)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def like_task(self, user):
    '''Celery task for liking random pin.'''
    try:
        keyword = Keyword.random.first()
        count = random.randint(config.MINIMUM_LIKE, config.MAXIMUM_LIKE)
        with lock(user.id):
            LikeScript()(user, keyword, count)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def comment_task(self, user):
    '''Celery task for commenting on random pin.'''
    try:
        keyword = Keyword.random.first()
        comments = Comment.random.all()
        count = random.randint(config.MINIMUM_COMMENT, config.MAXIMUM_COMMENT)
        with lock(user.id):
            CommentScript()(user, keyword, comments, count)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def follow_task(self, user):
    '''Celery task for following random users.'''
    try:
        keyword = Keyword.random.first()
        count = random.randint(config.MINIMUM_FOLLOW, config.MAXIMUM_FOLLOW)
        with lock(user.id):
            FollowScript()(user, keyword, count)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
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
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise
