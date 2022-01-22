import uuid
from datetime import datetime

from django.db import models

from AdNotifyManager.models.node import Node


class QueryLink(models.Model):
    class QueryLinkType(models.IntegerChoices):
        Base = 0,
        AVITO = 1

    class Meta(object):
        ordering = ['-data_create']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_create = models.DateTimeField(default=datetime.min)
    data_expired = models.DateTimeField(default=datetime.min, blank=True, null=True)
    query_link_type = models.IntegerField(
        choices=QueryLinkType.choices,
        default=QueryLinkType.Base,
    )
    name = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=300)
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, blank=True, null=True)
    filter_locate = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.name}'