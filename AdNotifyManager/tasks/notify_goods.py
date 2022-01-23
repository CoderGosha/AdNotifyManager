import logging

import telegram
from django.conf import settings

from AdNotifyManager.models import Goods, SubscriberChannelType, Subscriber


def send_goods(g: Goods):
    telegram_bot = getattr(settings, "TELEGRAM_BOT", None)
    if telegram_bot is None:
        raise Exception("Telegram token not found")

    bot = telegram.Bot(telegram_bot)
    subs = Subscriber.objects.filter(query_link=g.query_link).all()
    for s in subs:
        if s.subscriber_channel_type == SubscriberChannelType.Telegram:
            message = f"{g.name} \n{g.cost} \n \n{g.description} \n \n{g.goods_url}"
            logging.info(f"Send message: {message} to telegram: {s.channel_id} ")
            bot.send_message(s.channel_id, message, parse_mode=telegram.parsemode.ParseMode.HTML)
        else:
            logging.error(f"SubscriberChannelType: {s.subscriber_channel_type} unsupported")
