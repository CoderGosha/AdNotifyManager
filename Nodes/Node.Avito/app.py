import logging
import os

from loggerinitializer import initialize_logger
from workers.node_worker import NodeWorker


def main():
    API_KEY = os.environ.get('API_KEY')
    API_URL = os.environ.get('API_URL')
    NAME = os.environ.get('NAME')
    if API_KEY is None or API_URL is None or NAME is None:
        logging.error(f"Start fail: {NAME} with key: {API_KEY}, url: {API_URL}")
        return

    logging.info(f"Starting client: {NAME} with key: {API_KEY}, url: {API_URL}")
    worker = NodeWorker(API_URL, API_KEY, NAME)
    worker.start()


if __name__ == '__main__':
    initialize_logger("log")
    main()
