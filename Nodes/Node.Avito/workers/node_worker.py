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

    def start(self):
        super().start()
        self.do_main_work()
        
    def do_main_work(self):
        while True:
            try:
                links = self.get_query_link()
                goods = self.parser.get_data(links)
                self.send_goods(goods)
            except Exception as ex:
                self.increment_error()
                logging.error(ex)
            finally:
                time.sleep(self.timeout)

    def get_query_link(self):
        result = requests.get(self.api_url + "api/link", headers={'Authorization': f'Token {self.api_key}'},
                              params={"name": self.name})
        if result.status_code == 200:
            return result.json()
        else:
            self.increment_error()
            msg = f"Code: {result.status_code}, {result.text}"
            logging.info(msg)

    def send_goods(self, goods):
        for g in goods:
            result = requests.post(self.api_url + "api/goods/", headers={'Authorization': f'Token {self.api_key}'},
                                   json=g.__dict__)
            if result.status_code == 200:
                logging.info(f"Processing message: {g} - OK")
            elif result.status_code == 201:
                logging.info(f"Processing message: {g} - Create ok")
            else:
                self.increment_error()
                msg = f"Code: {result.status_code}, {result.text}"
                logging.info(msg)
