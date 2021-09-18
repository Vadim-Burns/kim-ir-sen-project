"""
This file contains configuration variables
"""

import os

# Database url
database_url = os.getenv("DATABASE_URL")

# Security key
security_key = os.environ.get("SECURITY_KEY")

# Static folder path(do not change this please)
static_folder = os.path.join(os.getcwd() + "/app/static")
