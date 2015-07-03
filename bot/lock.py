import logging

import redis

log = logging.getLogger('app')


class LockException(Exception):

    pass


class lock(object):

    def __init__(self, user_id):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.id = user_id

    def __enter__(self):
        self.lock = self.redis.lock(self.id)
        if self.lock.acquire(blocking=False):
            pass
        else:
            raise LockException

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if isinstance(ex_type, LockException):
            return False
        self.lock.release()
