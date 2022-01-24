import logging
import os


class AvitoBlockService:
    block_count = 0

    def __init__(self):
        pass

    def is_parsing(self) -> bool:
        if self.block_count > 2:
            self.do_block()

        return True

    def add_block(self):
        logging.error("AVITO IS BLOCKED")
        self.block_count += 1
        self.is_parsing()

    def do_block(self):
        message = "AVITO IS BLOCKED %i, BOT WAS TERMINATED" % self.block_count
        logging.error(message)
        # self.bot.send_message(self.chat_id, message, parse_mode=telegram.parsemode.ParseMode.HTML)
        os._exit(1)


