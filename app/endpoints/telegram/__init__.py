import telebot

import config
from endpoints import AbstractEndpoint
import inject
from services import AbstractKimService


class TelegramEndpoint(AbstractEndpoint):

    @inject.autoparams('kim_service')
    def __init__(self, token: str, kim_service: AbstractKimService):
        self._bot = telebot.TeleBot(token, parse_mode='Markdown', threaded=False)
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

    def _delete_message(self, message):
        self._bot.delete_message(chat_id=message.chat.id, message_id=message.id)

    def start(self, message):
        self._delete_message(message)

        self._bot.send_message(
            message.chat.id,
            "Welcome to Kim Ir Sen Bot!\n" +
            "Here you can save encrypt messages\n" +
            "Your confident is very important to our team, so every bot's message deletes after 10 seconds and your " +
            "messages delete immediately\n" +
            "To get help message use /help"
        )

    def help(self, message):
        self._delete_message(message)

        self._bot.send_message(
            message.chat.id,
            "/encrypt - encrypt message\n" +
            "Example: /encrypt hello there!\n" +
            "/decrypt - get encrypt message by key\n" +
            "Example: /decrypt key\n" +
            "/help - get this message"
        )

    def encrypt(self, message):
        self._delete_message(message)

        text = message.text.replace('/encrypt', '', 1)
        self._bot.send_message(
            message.chat.id,
            f"Your key is `{self._kim_service.save_note(text)}` will be deleted in 10 seconds"
        )

    def decrypt(self, message):
        self._delete_message(message)

        key = message.text.replace('/decrypt', '', 1)
        self._bot.send_message(
            message.chat.id,
            f"Your message is:\n`{self._kim_service.get_note(key)}`"
        )
