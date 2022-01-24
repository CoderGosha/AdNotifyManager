'''
    Метод проксирует запросы на нужного провайдера
'''
import json
import logging
import os
from sys import path

from selenium.webdriver.webkitgtk.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver

# from provider.communicator_provider import CommunicatorProvider


def _firefox_options_():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument('--headless')
    return options


class RequestService:
    #     driver = webdriver.Chrome(ChromeDriverManager().install(), options=_chrome_options_())
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=_firefox_options_())
    init_browser = False
    init_provider = False

    def __init__(self):
        self.provider = "LOCAL" #self.configuration.config['PROVIDER']['TYPE']

    def __init_browser__(self):
        import logging
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.INFO)
        self.driver.set_page_load_timeout(300)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(10)

        # self.proxy = configuration.config['PROXY']
    def __init_provider__(self):
        if self.provider == "LOCAL":
            pass

        elif self.provider == 'COMMUNICATOR':
            # api_key = self.configuration.config['PROVIDER']['COMMUNICATOR']['API_KEY']
            # api_url = self.configuration.config['PROVIDER']['COMMUNICATOR']['API_URL']
            # self.communicator_provider = CommunicatorProvider(api_url, api_key)
            pass

    def get(self, url) -> WebDriver:
        if not self.init_browser:
            self.__init_browser__()

        if not self.init_provider:
            self.__init_provider__()

        if self.provider == "LOCAL":
            self.driver.get(url)
        elif self.provider == 'COMMUNICATOR':
            # response, status = self.communicator_provider.request_get(url)
            #tmp_file = os.path.join(os.getcwd(), "tmp.html")
            #with open(tmp_file, "w", encoding="utf-8") as text_file:
            #    text_file.write(response)
            #if status:
            #    self.driver.get("file://" + tmp_file)
            #else:
            #    raise Exception(response)
            #logging.debug(response)
            pass
        else:
            logging.error(f"Unknown provider: {self.provider}")
            os._exit(1)

        return self.driver

