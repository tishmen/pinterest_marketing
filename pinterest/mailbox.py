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

    def login(self, email, host='imap.mail.yahoo.com', port=993):
        '''Login to imap with email address and password.'''
        self.imap = imaplib.IMAP4_SSL(host, port)
        self.imap.login(email.address, email.password)
        self.imap.select('"Inbox"')
        log.debug('Loged in to %s as %s', host, email.address)

    def get_html(self, sender='confirm@account.pinterest.com'):
        '''Return pinterest email message html.'''
        _, message_ids = self.imap.search(None, '(FROM {})'.format(sender))
        message_id = message_ids[0].decode('utf-8').split()[-1]
        if not message_id:
            raise EmailException
        _, message = self.imap.fetch(message_id, '(RFC822)')
        for part in email.message_from_bytes(message).walk():
            if part.get_content_type() == 'text/html':
                return quopri.decodestring(part.get_payload())

    def get_link(self):
        '''Parse html for pinterest confirmation link.'''
        soup = BeautifulSoup(self.get_html())
        link = soup.find_all('a')[4].get('href')
        log.debug('Got pinterest confirmation link')
        return link
