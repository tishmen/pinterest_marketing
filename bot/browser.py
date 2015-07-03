import json
import logging
import os
import random
import re
import time
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

from django.conf import settings

log = logging.getLogger('app')


class Browser(object):

    def get_profile(self, user_agent, proxy):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', user_agent.string)
        if proxy:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", proxy.host)
            profile.set_preference("network.proxy.http_port", proxy.port)
        profile.update_preferences()
        return profile

    def set_up(self, user):
        profile = self.get_profile(user.user_agent, user.proxy)
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.set_page_load_timeout(120)
        self.browser.implicitly_wait(30)
        for cookie in json.loads(user.cookies):
            self.browser.add_cookie(cookie)
        self.browser.maximize_window()
        log.debug('Set up browser instance')

    def destroy(self, user):
        user.cookies = json.dumps(self.browser.get_cookies())
        user.save()
        self.browser.quit()
        log.debug('Destroyed browser instance')

    def get_url(self, url):
        self.browser.get(url)
        log.debug('Got %s', url)

    def get_json(self):
        result = re.search('P.start.start\((.*)\);', self.browser.page_source)
        return json.loads(result.group(1))

    def get_element(self, key):
        return self.browser.find_element(*self.selectors[key])

    def get_elements(self, key):
        return self.browser.find_elements(*self.selectors[key])

    def click(self, name, element):
        element.click()
        log.debug('Clicked %s', name)
        time.sleep(random.randint(5, 10))

    def send_keys(self, name, element, text):
        element.send_keys(text)
        log.debug('Sent %s to %s', text, name)
        time.sleep(random.randint(5, 10))

    def select(self, name, element, value):
        options = Select(element)
        options.select_by_value(value)
        log.debug('Selected %s for %s', value, name)
        time.sleep(random.randint(5, 10))

    def clear(self, name, element):
        element.clear()

    def save_screenshot(self, user):
        file = '{}_{}.png'.format(user, time.strftime('%Y_%m_%d_%H_%M_%S'))
        path = os.path.join(settings.ERROR_DIR, file)
        self.browser.get_screenshot_as_file(path)

    def save_source(self, user):
        file = '{}_{}.html'.format(user, time.strftime('%Y_%m_%d_%H_%M_%S'))
        path = os.path.join(settings.ERROR_DIR, file)
        with open(path, 'w') as file:
            file.write(self.browser.page_source)

    @contextmanager
    def browser_handler(self, user):
        try:
            yield
        except WebDriverException:
            self.save_screenshot(user)
            self.save_source(user)
            raise
        finally:
            self.destroy(user)
