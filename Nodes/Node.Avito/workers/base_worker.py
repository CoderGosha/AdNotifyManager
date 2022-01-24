import datetime
import logging
import os
import threading
import time
import requests


class BaseWorker:
    def __init__(self, api_url, api_key, name):
        self.api_url = api_url
        self.api_key = api_key
        self.name = name
        self.version = "0.1"
        self.th_background_work = threading.Thread(target=self.do_background_work)
        self.th_background_work.daemon = True
        self.error_count = 0
        self.error_old_time = datetime.datetime.utcnow()
        self.timeout_default = 60
        self.timeout_long = 120
        self.timeout_very_long = 30 * 60
        self.timeout = self.timeout_default

    def start(self):
        self.th_background_work.start()

    def do_background_work(self):
        while True:
            try:
                self.ping()

            except Exception as ex:
                self.increment_error()
                logging.error(ex)
            finally:
                time.sleep(self.timeout)

    def increment_error(self):
        # Если время прошлой ошибки более часа то сбросим счетчик
        if (self.error_old_time + datetime.timedelta(hours=3)) < datetime.datetime.utcnow():
            self.error_count = 0
            self.timeout = self.timeout_default

        self.error_count += 1
        self.error_old_time = datetime.datetime.utcnow()

        if self.error_count > 1000:
            logging.info(f"Close App with error: {self.error_count}")
            os._exit(1)

        if self.error_count > 500:
            self.timeout = self.timeout_very_long
            return

        if self.error_count > 50:
            self.timeout = self.timeout_long
            return

    def ping(self):
        result = requests.post(self.api_url + "api/ping/", headers={'Authorization': f'Token {self.api_key}'},
                               json={'name': self.name})
        if result.status_code == 200:
            self.timeout = self.timeout_default
            return
        else:
            self.increment_error()
            msg = f"Code: {result.status_code}, {result.text}"
            logging.info(msg)