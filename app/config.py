"""
This file contains configuration variables
"""

import os

# Flask config
FLASK_PORT = os.environ.get('FLASK_PORT', 8080)
FLASK_ADDR = os.environ.get('FLASK_ADDR', '127.0.0.1')
FLASK_STATIC_FOLDER = os.path.join(os.getcwd() + "/endpoints/web/static")
FLASK_TEMPLATE_FOLDER = os.path.join(os.getcwd() + "/endpoints/web/templates")

# DATABASE CONFIG
_POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
_POSTGRES_USER = os.environ.get('POSTGRES_USER', 'kim')
_POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'kim')
_POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
_POSTGRES_NAME = os.environ.get('POSTGRES_NAME', 'kim')
DATABASE_CONNECT_URL = f"postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@{_POSTGRES_HOST}:{_POSTGRES_PORT}/{_POSTGRES_NAME}"

# Security key
SECURITY_KEY = os.environ.get("SECURITY_KEY")

# Telegram bot config
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
