from signal import signal, SIGTERM, SIGINT

import config
from di import DI
from endpoints import WebEndpoint, EndpointManager, TelegramEndpoint


def init_endpoint_manager() -> EndpointManager:
    endm = EndpointManager()

    # WEB(Flask)
    endm.add_endpoint(
        WebEndpoint(
            host=config.FLASK_ADDR,
            port=config.FLASK_PORT
        )
    )

    # Telegram
    endm.add_endpoint(
       TelegramEndpoint(
           token=config.TELEGRAM_BOT_TOKEN
       )
    )

    return endm


def serve():
    DI()

    endm = init_endpoint_manager()
    endm.run()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        try:
            endm.stop()
        except KeyboardInterrupt:
            pass
        print("Shutdown gracefully")

    signal(SIGTERM, handle_sigterm)
    signal(SIGINT, handle_sigterm)


if __name__ == '__main__':
    # logging.basicConfig(
    #     filename="kim.log",
    #     format='%(asctime)s: %(thread)d - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
    #     level=logging.DEBUG
    # )

    serve()
