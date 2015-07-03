import email
import imaplib
import logging
import quopri

from bs4 import BeautifulSoup

log = logging.getLogger('app')


class EmailException(Exception):

    pass


class MailBox(object):

    def login(self, email):
        self.imap = imaplib.IMAP4_SSL(email.host, email.port)
        self.imap.login(email.address, email.password)
        self.imap.select('Inbox')
        log.debug('Loged in to %s as %s', email.host, email.address)

    def get_html(self):
        _, ids = self.imap.search(None, '(FROM confirm@account.pinterest.com)')
        try:
            message_id = ids[0].decode('utf-8').split()[-1]
        except IndexError:
            log.error('Confirmation email not found')
            raise EmailException
        _, message = self.imap.fetch(message_id, '(RFC822)')
        return email.message_from_bytes(message[0][1]).get_payload()

    def get_link(self):
        soup = BeautifulSoup(quopri.decodestring(self.get_html()))
        link = soup.find_all('a')[4].get('href')
        log.debug('Got pinterest confirmation link')
        return link
