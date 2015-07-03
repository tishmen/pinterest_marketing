import logging
import random
import traceback
from contextlib import contextmanager

from celery import Task, shared_task
from constance import config

from .data import Data
from .lock import lock, LockException
from .mailbox import EmailException, MailBox
from .models import User
from .scripts import (
    CommentScript, ConfirmScript, CreateBoardsScript, CreateUserScript,
    FollowScript, InteractScript, LikeScript, LoginScript, RepinScript,
    SyncScript, UnfollowScript
)

log = logging.getLogger('app')


class BaseTask(Task):

    @contextmanager
    def task_handler(self, user_id, *args):
        try:
            with lock(user_id):
                yield
        except Exception as e:
            if isinstance(e, args):
                log.warn(
                    'Retrying %s %d time', self.name, self.request.retries
                )
                self.retry(countdown=60)
            log.error('Traceback: %s', traceback.format_exc())
            raise


class BasePeriodicTask(Task):

    abstract = True

    def get_countdown(self, countdown=0):
        return (
            countdown +
            random.randint(config.MINIMUM_COUNTDOWN, config.MAXIMUM_COUNTDOWN)
        )

    def run(self, task):
        countdown = self.get_countdown()
        for user in User.random.all():
            countdown = self.get_countdown(countdown)
            task.apply_async((user), countdown=countdown)


class LoginTask(BaseTask):

    def run(self, user):
        with self.task_handler(user.id, LockException):
            LoginScript().run(user)


class CreateUserTask(BaseTask):

    def run(self, user):
        with self.task_handler(user.id):
            CreateUserScript().run(user)


class InteractTask(BaseTask):

    def run(self, user):
        with self.task_handler(user.id):
            InteractScript().run(user)


class ConfirmTask(BaseTask):

    def get_link(self, user):
        mailbox = MailBox()
        mailbox.login(user.email)
        return mailbox.get_link()

    def run(self, user):
        with self.task_handler(user.id, EmailException, LockException):
                ConfirmScript().run(user, self.get_link(user))


class CreateBoardsTask(BaseTask, Data):

    def run(self, user):
        with self.task_handler(user.id, LockException):
            CreateBoardsScript().run(user, self.get_boards())


class SyncTask(BaseTask):

    def get_boards(self, user):
        return user.board_set(manager='random').all()

    def run(self, user):
        with self.task_handler(user.id, LockException):
            SyncScript().run(user, self.get_boards(user))


class RepinTask(BaseTask, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_REPIN, config.MAXIMUM_REPIN)

    def run(self, user):
        with self.task_handler(user.id, LockException):
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            RepinScript().run(user, keyword, board, self.get_count())


class LikeTask(BaseTask, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_LIKE, config.MAXIMUM_LIKE)

    def run(self, user):
        with self.task_handler(user.id, LockException):
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            LikeScript().run(user, keyword, self.get_count())


class CommentTask(BaseTask, Data):

    def get_count(self):
            return random.randint(
                config.MINIMUM_COMMENT, config.MAXIMUM_COMMENT
            )

    def run(self, user):
        with self.task_handler(user.id, LockException):
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            comments = self.get_comments(keyword.category)
            CommentScript().run(user, keyword, comments, self.get_count())


class FollowTask(BaseTask, Data):

    def get_count(self):
            return random.randint(config.MINIMUM_FOLLOW, config.MAXIMUM_FOLLOW)

    def run(self, user):
        with self.task_handler(user.id, LockException):
            board = self.get_board(user)
            keyword = self.get_keyword(board.category)
            FollowScript().run(user, keyword, self.get_count())


class UnfollowTask(BaseTask):

    def get_count(self):
            return random.randint(
                config.MINIMUM_UNFOLLOW, config.MAXIMUM_UNFOLLOW
            )

    def run(self, user):
        with self.task_handler(user.id, LockException):
            UnfollowScript().run(user, self.get_count())


@shared_task(bind=True, base=BasePeriodicTask)
def sync_periodic_task(self):
    self.run(SyncTask())


@shared_task(bind=True, base=BasePeriodicTask)
def repin_periodic_task(self):
    self.run(RepinTask())


@shared_task(bind=True, base=BasePeriodicTask)
def like_periodic_task(self):
    self.run(LikeTask())


@shared_task(bind=True, base=BasePeriodicTask)
def comment_periodic_task(self):
    self.run(CommentTask())


@shared_task(bind=True, base=BasePeriodicTask)
def follow_periodic_task(self):
    self.run(FollowTask())


@shared_task(bind=True, base=BasePeriodicTask)
def unfollow_periodic_task(self):
    self.run(UnfollowTask())
