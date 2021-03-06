import asyncio
import logging
import time
import uuid
from asyncio import Queue
from typing import List

from selenium.webdriver.common.by import By

from models.goods import Goods
from services.avito_block_service import AvitoBlockService
from services.request_service import RequestService


class AvitoService:
    def __init__(self):
        self.request_service = RequestService()
        self.block_service = AvitoBlockService()
        self.goods_cache = []

    def is_cache(self, g):
        key = g.external_id + g.goods_url
        if key in self.goods_cache:
            return True
        self.goods_cache.append(key)
        if len(self.goods_cache) > 1000:
            del self.goods_cache[:100]
        return False

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
        tmp_file = str(uuid.uuid4())
        filters_url = query_link['filter_url'].replace(" ", "").split(";")
        filters_url.remove("")

        try:
            driver = await self.request_service.get(query_link['url'], tmp_file)
            try:
                driver.find_element(By.CLASS_NAME, "icon-forbidden")
                self.block_service.add_block()
                return []
            except:
                pass
            # HACK
            wight = None

            for entry in driver.find_elements(By.XPATH, '//div[@itemtype="http://schema.org/Product"]'):
                link = entry.find_element(By.XPATH, './/a[@itemprop="url"]').get_attribute("href")
                description = entry.find_element(By.XPATH, './/meta[@itemprop="description"]').get_attribute("content")
                price = entry.find_element(By.XPATH, './/span[@itemtype="http://schema.org/Offer"]').text
                name = entry.find_element(By.XPATH, './/h3[@itemprop="name"]').text
                if not wight:
                    wight = entry.size["width"]
                if wight != entry.size["width"]:
                    #
                    logging.debug(f"Skip: {link}")
                    continue

                if len(link) > 1:
                    link = link.replace('file:///', 'https://avito.ru/')
                    g = Goods(link, name, query_link=query_link["id"], goods_url=link, cost=price,
                              description=description, locate='')
                    if self.is_filter_url(link, filters_url):
                        continue
                    if not self.is_cache(g):
                        goods.append(g)
                    count_element += 1
                    logging.debug(f"{name}, {price}, {link}")
                if count_element > 10:
                    break
        except Exception as ex:
            logging.error(ex)

        finally:
            self.request_service.temp_clean(tmp_file)

        logging.info('Completed: %s - %i' % (query_link['url'], len(goods)))
        # self.console.print("[bold cyan]Completed:[/bold cyan]", query_link['url'], "-",
        #                   f"[bold cyan] {len(goods)} [/bold cyan]")
        return goods

    def is_filter_url(self, link, filters_url):
        for f in filters_url:
            if f.strip() is not None and f.strip() != "":
                if link.find(f.strip()) != -1:
                    return True

        return False
