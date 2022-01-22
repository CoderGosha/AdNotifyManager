import uuid
from datetime import datetime

from django.db import models

from AdNotifyManager.models import QueryLink


class Subscriber(models.Model):
    class SubscriberChannelType(models.IntegerChoices):
        Telegram = 1

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_create = models.DateTimeField(default=datetime.min)
    data_expired = models.DateTimeField(default=datetime.min, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    channel_id = models.CharField(max_length=50, blank=True)
    subscriber_channel_type = models.IntegerField(
        choices=SubscriberChannelType.choices,
        default=SubscriberChannelType.Telegram,
        blank=True,
        null=True
    )
    query_link = models.ForeignKey(QueryLink, on_delete=models.SET_NULL, blank=True, null=True)
