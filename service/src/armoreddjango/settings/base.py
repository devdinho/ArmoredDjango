"""
Configurações base do Django.
Importa configurações modularizadas de outros arquivos.
"""

from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Site Configuration
SITE_ID = 1

ROOT_URLCONF = "armoreddjango.urls"

WSGI_APPLICATION = "armoreddjango.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Templates Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Import modular settings
from armoreddjango.settings.apps import *
from armoreddjango.settings.rest_framework import *
from armoreddjango.settings.cache import *
from armoreddjango.settings.internationalization import *
from armoreddjango.settings.static import *
