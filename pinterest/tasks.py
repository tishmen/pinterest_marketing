import logging
import random
import traceback

from celery import shared_task
from constance import config

from pinterest.models import User
from pinterest.mailbox import MailBox, EmailException
from pinterest.scripts import (
    CommentScript, ConfirmEmailScript, CreateBoardsScript, CreateUserScript,
    FollowScript, LikeScript, LoginScript, RepinScript, ScrapeScript,
    SyncScript, UnfollowScript
)
from pinterest_marketing.lock import LockException, lock
from store.models import Board, Comment, Keyword

log = logging.getLogger('pinterest_marketing')


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
def create_user_task(self, user):
    '''Celery task for creating pinterest user.'''
    try:
        with lock(user.id):
            CreateUserScript()(user)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def confirm_email_task(self, user):
    '''Celery task for confirming pinterest email.'''
    try:
        mailbox = MailBox()
        mailbox.login(user.email)
        link = mailbox.get_link()
        with lock(user.id):
            ConfirmEmailScript()(user, link)
    except EmailException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=300)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
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
        with lock(user.id):
            CreateBoardsScript()(user, boards)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def sync_task(self, user):
    '''Celery task for syncing pinterest user with local database.'''
    try:
        boards = user.board_set.all()
        with lock(user.id):
            SyncScript()(user, boards)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True, max_retries=1)
def repin_task(self, user):
    '''Celery task for repinning random pins.'''
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
    '''Celery task for liking random pins.'''
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
    '''Celery task for commenting on random pins.'''
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


@shared_task(bind=True, max_retries=1)
def scrape_task(self, user):
    '''Celery task for scraping random pins.'''
    try:
        keyword = Keyword.random.first()
        with lock(user.id):
            ScrapeScript()(user, keyword)
    except LockException:
        log.warn('Retrying task %d time', self.request.retries)
        self.retry(countdown=100)
    except Exception:
        log.error('Traceback: %s', traceback.format_exc())
        raise


@shared_task(bind=True)
def sync_periodic_task(self, user):
    '''Periodic celery task for syncing pinterest users.'''
    for user in User.available.all():
        sync_task.delay(user)


@shared_task(bind=True)
def repin_periodic_task(self, user):
    '''Periodic celery task for repining random users.'''
    for user in User.available.all():
        repin_task.delay(user)


@shared_task(bind=True)
def like_periodic_task(self, user):
    '''Periodic celery task for liking random users.'''
    for user in User.available.all():
        like_task.delay(user)


@shared_task(bind=True)
def comment_periodic_task(self, user):
    '''Periodic celery task for commenting on random users.'''
    for user in User.available.all():
        comment_task.delay(user)


@shared_task(bind=True)
def follow_periodic_task(self, user):
    '''Periodic celery task for following random users.'''
    for user in User.available.all():
        follow_task.delay(user)


@shared_task(bind=True)
def unfollow_periodic_task(self, user):
    '''Periodic celery task for unfollowing random users.'''
    for user in User.available.all():
        unfollow_task.delay(user)


@shared_task(bind=True)
def scrape_periodic_task(self, user):
    '''Periodic celery task for scraping random pins.'''
    for user in User.available.all():
        scrape_task.delay(user)
