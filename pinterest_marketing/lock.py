import logging

import redis

log = logging.getLogger('pinterest_marketing')


class LockException(Exception):

    '''Exception for failed lock acquisition.'''

    pass


class lock(object):

    '''Context aware class for resource locking.'''

    def __init__(self, id):
        self.id = id

    def __enter__(self):
        '''Acquire lock or raise LockException.'''
        redis_ = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.lock = redis_.lock(self.id)
        if not self.lock.acquire(blocking=False):
            log.debug('Could not acquire lock %s', self.id)
            raise LockException

    def __exit__(self, exception_type, exception_value, exception_traceback):
        '''Release lock or reraise LockException.'''
        if isinstance(exception_type, LockException):
            return False
        self.lock.release()
