import os

from dotenv import load_dotenv

from armoreddjango.settings.base import *

SITE_ID = 1

load_dotenv(override=True)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").lower() in (
    "true",
    "1",
    "yes",
)

POSTGRES_DB = "armoreddjango_db"
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "armoreddjango_db"
DB_PORT = os.getenv("DB_PORT", 5432)

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    os.getenv("SYSTEM_URL", "insert-your-domain-here.com"),
]

# Adicionar hosts adicionais se configurados
if os.getenv("VM_IP"):
    ALLOWED_HOSTS.append(os.getenv("VM_IP"))
if os.getenv("VITE_SYSTEM_URL"):
    ALLOWED_HOSTS.append(os.getenv("VITE_SYSTEM_URL"))

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8003",
    "http://localhost:5174",  # Frontend development
    "http://0.0.0.0:8003",
    f"https://{os.getenv('SYSTEM_URL', 'insert-your-domain-here.com')}",
]

# Adicionar origins adicionais se configurados
if os.getenv("SYSTEM_URL") and os.getenv("SYSTEM_URL") != "insert-your-domain-here.com":
    CSRF_TRUSTED_ORIGINS.append(os.getenv("SYSTEM_URL"))

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

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

# Configurações de Email
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")
