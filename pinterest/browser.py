import json
import logging
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from pinterest_marketing.settings import ERROR_DIR

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
        self.browser.set_page_load_timeout(120)
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
        time.sleep(5)

    def send_keys(self, name, element, text):
        '''Set html element input to text.'''
        element.send_keys(text)
        log.debug('Sent %s to %s', text, name)
        time.sleep(5)

    def select(self, name, element, value):
        '''Select option by value.'''
        options = Select(element)
        options.select_by_value(value)
        log.debug('Selected %s for %s', value, name)
        time.sleep(5)

    def clear(self, name, element):
        '''Clear element input.'''
        element.clear()

    def save_screenshot(self, user):
        '''Save screenshot to disk.'''
        path = os.path.join(
            ERROR_DIR, '{}_{}.png'.format(
                user, time.strftime('%Y_%m_%d_%H_%M_%S')
            )
        )
        self.browser.get_screenshot_as_file(path)

    def save_source(self, user):
        '''Save page source to disk.'''
        path = os.path.join(
            ERROR_DIR, '{}_{}.html'.format(
                user, time.strftime('%Y_%m_%d_%H_%M_%S')
            )
        )
        with open(path, 'w') as file:
            file.write(self.browser.page_source)
