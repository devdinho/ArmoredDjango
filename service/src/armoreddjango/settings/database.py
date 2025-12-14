"""
Configurações de banco de dados.
"""

import os

POSTGRES_DB = "armoreddjango_db"
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "armoreddjango_db"
DB_PORT = os.getenv("DB_PORT", 5432)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}
