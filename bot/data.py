import random

from constance import config

from data.models import Board, Comment, Keyword


class DataException(Exception):

    pass


class Data(object):

    def get_or_raise(self, name, data):
        if not data:
            raise DataException('No {} data for {}'.format(name, self.name))
        return data

    def get_boards(self):
        count = random.randint(config.MINIMUM_BOARD, config.MAXIMUM_BOARD)
        boards = Board.random.all()[:count]
        return self.get_or_raise('board', boards)

    def get_board(self, user):
        board = user.board_set(manager='random').first()
        return self.get_or_raise('board', board)

    def get_keyword(self, category):
        keyword = Keyword.random.filter(category=category).first()
        return self.get_or_raise('keyword', keyword)

    def get_comments(self, category):
        comments = Comment.random.filter(category=category).all()
        return self.get_or_raise('comment', comments)
