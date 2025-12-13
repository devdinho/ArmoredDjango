import os
import sys
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Detecta se está rodando testes
TESTING = "pytest" in sys.modules or "test" in sys.argv


DEFAULT_APPS = [
    "materialdash",
    "materialdash.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "armoreddjango",
    "authentication",
    "utils",
]

OTHER_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "simple_history",
    "corsheaders",
    "drf_yasg",
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + OTHER_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "armoreddjango.urls"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Aplica rate limiting apenas em produção, não em testes
if not TESTING:
    REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ]
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {"anon": "5/second", "user": "20/second"}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # 15 Minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=7),  # 7 Days
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "SECURITY_REQUIREMENTS": [{"Bearer": []}],
}

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

WSGI_APPLICATION = "armoreddjango.wsgi.application"

AUTH_USER_MODEL = "authentication.profile"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "authentication.validators.ComplexPasswordValidator",
    },
]

TIME_ZONE = "America/Araguaina"

DATE_FORMAT = "%d/%m/%Y"

LANGUAGE_CODE = "pt-BR"

USE_I18N = True

USE_TZ = True

MEDIA_URL = "media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGIN_URL = "/admin/login/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-armoreddjango-cache",
    }
}

CACHE_TIMEOUT = 60 * 60  # 1 hour
CACHE_TIMEOUT_SHORT = 5 * 60  # 5 minutes
