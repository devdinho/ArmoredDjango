"""
Configurações de cache.
"""

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-armoreddjango-cache",
    }
}

CACHE_TIMEOUT = 60 * 60  # 1 hour
CACHE_TIMEOUT_SHORT = 5 * 60  # 5 minutes
