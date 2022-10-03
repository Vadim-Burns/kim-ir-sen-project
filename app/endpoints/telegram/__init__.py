import telebot

from endpoints import AbstractEndpoint
import inject
from services import AbstractKimService
from threading import Thread
import time


class TelegramEndpoint(AbstractEndpoint):

    @inject.autoparams('kim_service')
    def __init__(self, token: str, kim_service: AbstractKimService):
        self._bot = telebot.TeleBot(token, parse_mode='Markdown', threaded=False)
        self._kim_service = kim_service
        self._delete_time = 30

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

        self._bot.add_message_handler(
            self._bot._build_handler_dict(
                self.help,
                commands=['help']
            )
        )

        self._bot.add_message_handler(
            self._bot._build_handler_dict(
                self.encrypt,
                commands=['encrypt']
            )
        )

        self._bot.add_message_handler(
            self._bot._build_handler_dict(
                self.decrypt,
                commands=['decrypt']
            )
        )

    def run(self):
        self._bot.infinity_polling()

    def get_name(self) -> str:
        return "Telegram bot"

    def _delete_message(self, message, timeout=None):
        if timeout is None:
            self._bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        else:
            def foo():
                time.sleep(timeout)
                self._bot.delete_message(chat_id=message.chat.id, message_id=message.id)

            Thread(target=foo).start()

    def start(self, message):
        self._delete_message(message)

        dm = self._bot.send_message(
            message.chat.id,
            "Welcome to Kim Ir Sen Bot!\n" +
            "Here you can save encrypt messages\n" +
            f"Your confident is very important to our team, so every bot's message deletes after {self._delete_time} seconds and your " +
            "messages delete immediately\n" +
            "To get help message use /help"
        )
        self._delete_message(dm, self._delete_time)

    def help(self, message):
        self._delete_message(message)

        dm = self._bot.send_message(
            message.chat.id,
            "/encrypt - encrypt message\n" +
            "Example: /encrypt hello there!\n" +
            "/decrypt - get encrypt message by key\n" +
            "Example: /decrypt key\n" +
            "/help - get this message"
        )
        self._delete_message(dm, self._delete_time)

    def encrypt(self, message):
        self._delete_message(message)

        text = message.text.replace('/encrypt', '', 1)
        dm = self._bot.send_message(
            message.chat.id,
            f"Your key is `{self._kim_service.save_note(text)}` will be deleted in {self._delete_time} seconds"
        )
        self._delete_message(dm, self._delete_time)

    def decrypt(self, message):
        self._delete_message(message)

        key = message.text.replace('/decrypt', '', 1)
        note = self._kim_service.get_note(key)
        if note is None:
            dm = self._bot.send_message(
                message.chat.id,
                "Wrong key"
            )
        else:
            dm = self._bot.send_message(
                message.chat.id,
                f"Your message is:\n`{self._kim_service.get_note(key)}`"
            )
        self._delete_message(dm, self._delete_time)
