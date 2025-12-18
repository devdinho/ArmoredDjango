"""
Utils module for ArmoredDjango.

This module provides utility functions and constants for the application.

Remember to import specific functions or constants as needed.
Remember import cache_utils functions from service/src/utils/cache_utils.py

Para exemplos de uso de email, veja:
- utils/email_examples.py - Exemplos práticos prontos para copiar
- utils/EMAIL_QUICK_START.md - Guia rápido de uso
"""

from utils.constants import *  # noqa F401 F403

# Email functions
from utils.emails import build_email_html  # noqa F401
from utils.emails import load_email_template  # noqa F401
from utils.emails import send_email  # noqa F401
from utils.emails import send_notification_email  # noqa F401
from utils.emails import send_password_reset_email  # noqa F401
from utils.emails import send_welcome_email  # noqa F401

# Validation and formatting functions
from utils.useful_functions import format_cpf  # noqa F401
from utils.useful_functions import format_phone  # noqa F401
from utils.useful_functions import sanitize_string  # noqa F401
from utils.useful_functions import validate_cpf  # noqa F401
from utils.useful_functions import validate_phone  # noqa F401
