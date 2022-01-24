
class Goods:
    def __init__(self, external_id: str, name: str, cost: str, description: str, locate: str, query_link: str,
                 goods_url: str):
        self.query_link = query_link
        self.locate = locate
        self.description = description
        self.cost = cost
        self.goods_url = goods_url
        self.name = name
        self.external_id = external_id

    def __str__(self):
        return f"{self.name} - {self.goods_url}"

