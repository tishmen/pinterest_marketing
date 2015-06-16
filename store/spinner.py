import random
import re


class TextSpinner(object):

    '''Class containing text spinning functionality.'''

    def select(self, match):
        '''Select randomly one of the words in a spintax group'''
        return random.choice(match.group(1).split('|'))

    def spin(self, string):
        '''Spin spintax formated string.'''
        r = re.compile('{([^{}]*)}')
        while True:
            string, n = r.subn(self.select, string)
            if not n:
                break
        return string.strip()
