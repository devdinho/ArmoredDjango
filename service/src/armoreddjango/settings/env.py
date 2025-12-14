"""
Configurações de ambiente carregadas a partir de variáveis de ambiente.
Este arquivo carrega todas as configurações específicas do ambiente (dev/prod).
"""

from dotenv import load_dotenv

# Carrega variáveis de ambiente primeiro
load_dotenv(override=True)

# Importa configurações base
from armoreddjango.settings.base import *
from armoreddjango.settings.database import *
from armoreddjango.settings.email import *

# Importa configurações específicas de ambiente
from armoreddjango.settings.security import *
