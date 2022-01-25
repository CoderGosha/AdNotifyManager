import datetime
import json
import logging
import os
import threading
import time

import requests

from services.avito_service import AvitoService
from workers.base_worker import BaseWorker


class NodeWorker(BaseWorker):
    def __init__(self, api_url, api_key, name):
        super().__init__(api_url, api_key, name)
        self.parser = AvitoService()
        self.hour_begin = int(os.environ.get('HOUR_BEGIN', -1))
        self.hour_end = int(os.environ.get('HOUR_END', -1))
        self.timeout_periodic = int(os.environ.get('PERIODIC_MINUTES', 1))
        logging.info(
            f"Staring node: {self.name} with periodic: {self.timeout_periodic} minutes, {self.hour_begin}/{self.hour_end}")

    def start(self):
        super().start()
        self.do_main_work()

    def do_main_work(self):
        while True:
            try:
                if self.is_work_time():
                    links = self.get_query_link()
                    goods = self.parser.get_data(links)
                    self.send_goods(goods)
            except Exception as ex:
                self.increment_error()
                logging.error(ex)
            finally:
                time.sleep(self.timeout_periodic * 60)

    def get_query_link(self):
        result = requests.get(self.api_url + "api/link", headers={'Authorization': f'Token {self.api_key}'},
                              params={"name": self.name})
        if result.status_code == 200:
            return result.json()
        else:
            self.increment_error()
            msg = f"Code: {result.status_code}, {result.text}"
            logging.info(msg)
        return []

    def send_goods(self, goods):
        for g in goods:
            result = requests.post(self.api_url + "api/goods/", headers={'Authorization': f'Token {self.api_key}'},
                                   json=g.__dict__)
            if result.status_code == 200:
                logging.debug(f"Processing message: {g} - OK")
            elif result.status_code == 201:
                logging.debug(f"Processing message: {g} - Create ok")
            else:
                self.increment_error()
                msg = f"Code: {result.status_code}, {result.text}"
                logging.info(msg)

    def is_work_time(self):
        if self.hour_begin == -1 or self.hour_end == -1:
            return True

        current_time = datetime.datetime.utcnow()
        if (current_time.hour >= self.hour_begin) and (current_time.hour < self.hour_end):
            return True
        return False
