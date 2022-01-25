import asyncio
import datetime
import logging
import os
import time

import aiohttp
import requests


class CommunicatorProvider:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.timeout_minutes = 1

    async def request_get(self, request) -> (str, bool):
        result = requests.post(self.api_url + "api/provider/", headers={'Authorization': f'Token {self.api_key}'},
                               json={'event_type': 1, 'request': request})
        if result.status_code != 200:
            msg = f"Code: {result.status_code}, {result.text}"
            return msg, False

        logging.debug(f"Processing request: {request} - {result.json()}")
        event_id = result.json()['id']
        date_time_start = datetime.datetime.now()
        timeout = date_time_start + datetime.timedelta(minutes=self.timeout_minutes)
        while datetime.datetime.now() < timeout:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url + "api/provider",
                                       headers={'Authorization': f'Token {self.api_key}'},
                                       params={"id": event_id}) as result_command:
                    await result_command.text()

                    if result_command.status == 200:
                        response = await result_command.json()
                        if response['success'] is None:
                            logging.debug('Waiting response')
                            await asyncio.sleep(5)
                        else:
                            logging.info(f"Request: {request} - {event_id} - ok")
                            return response['response'], response['success']

                    else:
                        msg = f"Code: {result_command.status}, {result_command.text}"
                        logging.warning(msg)
                        return msg, False

                    await asyncio.sleep(1)
            await session.close()
        return "", False


def main():
    API_KEY = os.environ.get('API_KEY')
    API_URL = os.environ.get('API_URL')
    if API_KEY is None or API_URL is None:
        logging.error(f"Start fail with key: {API_KEY}, url: {API_URL}")
        return

    provider = CommunicatorProvider(api_url=API_URL, api_key=API_KEY)
    request = "https://docs.djangoproject.com/en/3.2/ref/models/fields/"
    result, status = provider.request_get(request)
    logging.info(f"Request: {request}, status: {status}, response: {result}")


if __name__ == '__main__':
    from loggerinitializer import initialize_logger

    initialize_logger("log")
    main()
