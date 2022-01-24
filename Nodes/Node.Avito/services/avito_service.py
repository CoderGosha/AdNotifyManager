from typing import List

from models.goods import Goods


class AvitoService:
    def __init__(self):
        pass

    def get_data(self, links) -> List[Goods]:
        goods = []
        for l in links:
            g = Goods("126", "Test1", query_link=l["id"], goods_url="http://test.com", cost='100500', description='',
                      locate='')
            goods.append(g)
        return goods
