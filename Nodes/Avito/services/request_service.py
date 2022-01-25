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
from provider.communicator_provider import CommunicatorProvider


def _firefox_options_():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument('--headless')
    return options


class RequestService:
    init_browser = False
    init_provider = False

    def __init__(self):
        self.provider = os.environ.get("PROVIDER", "LOCAL")

    def __init_browser__(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=_firefox_options_())
        import logging
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.INFO)
        self.driver.set_page_load_timeout(300)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(10)
        self.init_browser = True

        # self.proxy = configuration.config['PROXY']

    def __init_provider__(self):
        if self.provider == "LOCAL":
            pass

        elif self.provider == 'COMMUNICATOR':
            api_key = os.environ.get("PROVIDER_API_KEY", None)
            api_url = os.environ.get("PROVIDER_API_URL", None)
            if api_key is None or api_url is None:
                logging.error(f"Provider PROVIDER_API_KEY: {api_key} or PROVIDER_API_URL: {api_url} is None:")
                os._exit(1)

            self.communicator_provider = CommunicatorProvider(api_url, api_key)
            pass
        self.init_provider = True

    async def get(self, url, tmp_file=None) -> WebDriver:
        if not self.init_browser:
            self.__init_browser__()

        if not self.init_provider:
            self.__init_provider__()

        if self.provider == "LOCAL":
            self.driver.get(url)
        elif self.provider == 'COMMUNICATOR':
            response, status = await self.communicator_provider.request_get(url)
            tmp_file = os.path.join(os.getcwd(), tmp_file)
            with open(tmp_file, "w", encoding="utf-8") as text_file:
                text_file.write(response)
            if status:
                self.driver.get("file://" + tmp_file)
            else:
                raise Exception(response)
            logging.debug(response)
            pass
        else:
            logging.error(f"Unknown provider: {self.provider}")
            os._exit(1)

        return self.driver

    def temp_clean(self, tmp_file=None):
        if tmp_file is None:
            return
        if os.path.isfile(os.path.join(os.getcwd(), tmp_file)):
            os.remove(os.path.join(os.getcwd(), tmp_file))
