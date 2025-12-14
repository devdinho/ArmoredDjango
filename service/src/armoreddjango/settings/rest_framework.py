"""
Configurações do Django REST Framework e JWT.
"""

import sys
from datetime import timedelta

# Detecta se está rodando testes
TESTING = "pytest" in sys.modules or "test" in sys.argv

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

# Simple JWT Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # 15 Minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_LIFETIME": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=7),  # 7 Days
    "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=7),  # 7 Days
}

# Swagger/OpenAPI Configuration
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "SECURITY_REQUIREMENTS": [{"Bearer": []}],
}
