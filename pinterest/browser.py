import json
import logging
import random
import re
import time

from selenium import webdriver

log = logging.getLogger('pinterest_marketing')


class Browser(object):

    '''Base class for browser functionality.'''

    def get_profile(self, user_agent, proxy):
        '''Return firefox profile with set proxy and user agent.'''
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', user_agent.string)
        if proxy:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", proxy.host)
            profile.set_preference("network.proxy.http_port", proxy.port)
        profile.update_preferences()
        return profile

    def set_up(self, user):
        '''Set up and start browser instance.'''
        profile = self.get_profile(user.user_agent, user.proxy)
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.set_page_load_timeout(60)
        self.browser.implicitly_wait(30)
        for cookie in json.loads(user.cookies):
            self.browser.add_cookie(cookie)
        self.browser.maximize_window()
        log.debug('Set up browser instance')

    def destroy(self, user):
        '''Destroy browser instance.'''
        user.cookies = json.dumps(self.browser.get_cookies())
        user.save()
        self.browser.quit()
        log.debug('Destroyed browser instance')

    def get_url(self, url):
        '''Navigate to url location.'''
        self.browser.get(url)
        log.debug('Got %s', url)

    def get_element(self, key):
        '''Return html element.'''
        return self.browser.find_element(*self.selectors[key])

    def get_elements(self, key):
        '''Return html elements.'''
        return self.browser.find_elements(*self.selectors[key])

    def get_json(self):
        '''Return json from current page source. Pinterest specific.'''
        result = re.search('P.start.start\((.*)\);', self.browser.page_source)
        return json.loads(result.group(1))

    def click(self, name, element):
        '''Dispatch click event on html element.'''
        element.click()
        log.debug('Clicked %s', name)
        time.sleep(random.uniform(5, 10))

    def send_keys(self, name, element, text):
        '''Set html element input to text.'''
        element.send_keys(text)
        log.debug('Sent %s to %s', text, name)
        time.sleep(random.uniform(5, 10))
