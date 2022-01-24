import uuid
from datetime import datetime

from django.db import models

from AdNotifyManager.models import QueryLink


class Goods(models.Model):
    class Meta:
        verbose_name = 'Goods'
        verbose_name_plural = 'Goods'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=250, blank=True, null=True)
    data_create = models.DateTimeField(default=datetime.min)
    name = models.CharField(max_length=50)
    cost = models.CharField(max_length=50)
    description = models.CharField(max_length=1200)
    locate = models.CharField(max_length=50, blank=True, null=True)
    query_link = models.ForeignKey(QueryLink, on_delete=models.SET_NULL, blank=True, null=True)
    goods_url = models.CharField(max_length=250, blank=True, null=True)
