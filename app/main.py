import config
from di import DI
from server import app as flask_app

if __name__ == '__main__':
    # logging.basicConfig(
    #     filename="kim.log",
    #     format='%(asctime)s: %(thread)d - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
    #     level=logging.DEBUG
    # )

    DI()
    flask_app.run(host=config.FLASK_ADDR, port=config.FLASK_PORT)
