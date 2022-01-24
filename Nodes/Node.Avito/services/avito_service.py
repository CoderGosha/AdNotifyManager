import asyncio
import logging
import time
from asyncio import Queue
from typing import List

from models.goods import Goods
from services.avito_block_service import AvitoBlockService
from services.request_service import RequestService


class AvitoService:
    def __init__(self):
        self.request_service = RequestService()
        self.block_service = AvitoBlockService()
        self.goods_cache = []

    def get_data(self, links) -> List[Goods]:
        ioloop = asyncio.get_event_loop()
        goods = ioloop.run_until_complete(self.a_parsings(links))
        # ioloop.close()

        return goods

    """
        Запускаем пул задач
    """

    async def a_parsings(self, links):
        goods = []
        futures = [self.a_prasing_link(link) for link in links]
        for i, future in enumerate(asyncio.as_completed(futures)):
            result = await future
            goods.extend(result)

        return goods

    """
        Выполняем парсинг каждого элемента
    """

    async def a_prasing_link(self, query_link) -> List[Goods]:
        goods = []
        count_element = 0
        try:
            # TODO async
            driver = self.request_service.get(query_link['url'])
            try:
                driver.find_element_by_class_name("icon-forbidden")
                self.block_service.add_block()
                return []
            except:
                pass
            # HACK
            wight = None

            for entry in driver.find_elements_by_xpath('//div[@itemtype="http://schema.org/Product"]'):
                link = entry.find_element_by_xpath('.//a[@itemprop="url"]').get_attribute("href")
                description = entry.find_element_by_xpath('.//meta[@itemprop="description"]').get_attribute("content")
                price = entry.find_element_by_xpath('.//span[@itemtype="http://schema.org/Offer"]').text
                name = entry.find_element_by_xpath('.//h3[@itemprop="name"]').text
                if not wight:
                    wight = entry.size["width"]
                if wight != entry.size["width"]:
                    #
                    logging.info(f"Skip: {link}")
                    continue

                if len(link) > 1:
                    link = link.replace('file:///', 'https://avito.ru/')
                    g = Goods(link, name, query_link=query_link["id"], goods_url=link, cost=price,
                              description=description, locate='')
                    if not self.is_cache(g):
                        goods.append(g)
                    count_element += 1
                    logging.debug(f"{name}, {price}, {link}")
                if count_element > 10:
                    break
        except Exception as ex:
            logging.error(ex)

        finally:
            pass

        logging.info('Parsing completed: %s - %i' % (query_link['url'], len(goods)))
        return goods

    def is_cache(self, g):
        key = g.external_id + g.goods_url
        if key in self.goods_cache:
            return True
        self.goods_cache.append(key)
        if len(self.goods_cache) > 1000:
            del self.goods_cache[:100]
        return False
