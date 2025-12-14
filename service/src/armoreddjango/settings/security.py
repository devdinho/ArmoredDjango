"""
Configurações de segurança e autenticação.
"""

import os

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"

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

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").lower() in (
    "true",
    "1",
    "yes",
)

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

# Auth Configuration
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

LOGIN_URL = "/admin/login/"
