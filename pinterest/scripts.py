import logging

from pinterest.browser import Browser

log = logging.getLogger('pinterest_marketing')


class CreateUserScript(Browser):

    '''Create user on pinterest.'''

    def __call__(self, user):
        '''Run selenium script for CreateUserScript.'''
        log.debug('Called CreateUserScript with args %s', user)


class ConfirmEmailScript(Browser):

    '''Confirm email on pinterest.'''

    def __call__(self, user):
        '''Run selenium script for ConfirmEmailScript.'''
        log.debug('Called ConfirmEmailScript with args %s', user)


class LoginScript(Browser):

    '''Login user on pinterest.'''

    def __call__(self, user):
        '''Run selenium script for LoginScript.'''
        log.debug('Called LoginScript with args %s', user)


class CreateBoardsScript(Browser):

    '''Create boards on pinterest.'''

    def __call__(self, user, boards):
        '''Run selenium script for CreateBoardsScript.'''
        log.debug('Called CreateBoardsScript with args %s, %s', user, boards)


class RepinScript(Browser):

    '''Repin random pins on pinterest.'''

    def __call__(self, user, keyword, boards, count):
        '''Run selenium script for RepinScript.'''
        log.debug(
            'Called RepinScript with args %s, %s, %s, %d',
            user, keyword, boards, count
        )


class LikeScript(Browser):

    '''Like random pins on pinterest.'''

    def __call__(self, user, keyword, count):
        '''Run selenium script for LikeScript.'''
        log.debug(
            'Called LikeScript with args %s, %s, %d', user, keyword, count
        )


class CommentScript(Browser):

    '''Comment on random pins on pinterest.'''

    def __call__(self, user, keyword, comments, count):
        '''Run selenium script for CommentScript.'''
        log.debug(
            'Called CommentScript with args %s, %s, %s, %d',
            user, keyword, comments, count
        )


class FollowScript(Browser):

    '''Follow random users on pinterest.'''

    def __call__(self, user, keyword, count):
        '''Run selenium script for FollowScript.'''
        log.debug(
            'Called FollowScript with args %s, %s, %d', user, keyword, count
        )


class UnfollowScript(Browser):

    '''Unfollow random users on pinterest.'''

    def __call__(self, user, count):
        '''Run selenium script for UnfollowScript.'''
        log.debug('Called UnfollowScript with args %s, %d', user, count)
