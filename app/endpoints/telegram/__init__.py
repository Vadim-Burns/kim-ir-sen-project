import telebot

import config
from endpoints import AbstractEndpoint
import inject
from services import AbstractKimService


class TelegramEndpoint(AbstractEndpoint):

    @inject.autoparams('kim_service')
    def __init__(self, token: str, kim_service: AbstractKimService):
        self._token = token
        self._bot = telebot.TeleBot(token, parse_mode='html', threaded=False)
        self._kim_service = kim_service

        self._init_mapping()

    def _init_mapping(self):
        """
        Init bot message mapping
        """
        self._bot.add_message_handler(
            self._bot._build_handler_dict(
                self.start,
                commands=['start']
            )
        )

    def run(self):
        self._bot.infinity_polling()

    def get_name(self) -> str:
        return "Telegram bot"

    def start(self, message):
        print(message)
        self._bot.send_message(message.chat.id, "Hello there!")


if __name__ == '__main__':
    import multiprocessing as mp

    tg = TelegramEndpoint(config.TELEGRAM_BOT_TOKEN)
    mp.Process(target=tg.run).start()
