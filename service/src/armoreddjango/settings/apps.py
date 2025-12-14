"""
Configurações de aplicações Django.
"""

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
