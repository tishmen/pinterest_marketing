import email
import imaplib
import logging
import quopri

from bs4 import BeautifulSoup

log = logging.getLogger('pinterest_marketing')


class EmailException(Exception):

    '''Exception for failed email acquisition.'''

    pass


class MailBox(object):

    '''IMAP connection to a Yahoo.'''

    def login(self, email):
        '''Login to imap with email address and password.'''
        self.imap = imaplib.IMAP4_SSL('imap.mail.yahoo.com', 993)
        self.imap.login(email.address, email.password)
        self.imap.select('"Inbox"')
        log.debug('Loged in to imap.mail.yahoo.com as %s', email.address)

    def get_html(self):
        '''Return pinterest email raw html content.'''
        _, ids = self.imap.search(None, '(FROM confirm@account.pinterest.com)')
        try:
            message_id = ids[0].decode('utf-8').split()[-1]
        except IndexError:
            raise EmailException('Comfirmation email not found')
        _, message = self.imap.fetch(message_id, '(RFC822)')
        for part in email.message_from_bytes(message).walk():
            if part.get_content_type() == 'text/html':
                return part.get_payload()

    def get_link(self):
        '''Parse html for pinterest confirmation link.'''
        soup = BeautifulSoup(quopri.decodestring(self.get_html()))
        link = soup.find_all('a')[4].get('href')
        log.debug('Got pinterest confirmation link')
        return link
