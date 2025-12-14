# Configurações Modularizadas do Django

Esta estrutura organiza as configurações do Django em módulos separados por responsabilidade, facilitando a manutenção e compreensão do código.

## Estrutura de Arquivos

```
settings/
├── __init__.py              # Ponto de entrada (importa env.py)
├── base.py                  # Configurações base do Django
├── env.py                   # Carrega variáveis de ambiente
├── apps.py                  # INSTALLED_APPS e MIDDLEWARE
├── rest_framework.py        # Django REST Framework e JWT
├── database.py              # Configuração do banco de dados
├── cache.py                 # Configuração de cache
├── email.py                 # Configuração de e-mail
├── security.py              # Segurança, autenticação e CORS
├── internationalization.py  # i18n e localização
├── static.py                # Arquivos estáticos e mídia
└── README.md                # Este arquivo
```

## Módulos

### `base.py`

Configurações principais do Django que não dependem de ambiente:

- `BASE_DIR`, `SITE_ID`
- `ROOT_URLCONF`, `WSGI_APPLICATION`
- `TEMPLATES`
- Importa todos os outros módulos de configuração

### `env.py`

Carrega as variáveis de ambiente e importa configurações específicas:

- Carrega `.env` usando `python-dotenv`
- Importa `base.py`, `security.py`, `database.py`, `email.py`

### `apps.py`

Gerencia aplicações Django:

- `INSTALLED_APPS` (organizados em DEFAULT_APPS, LOCAL_APPS, OTHER_APPS)
- `MIDDLEWARE`

### `rest_framework.py`

Configurações da API REST:

- `REST_FRAMEWORK` (permissões, autenticação, throttling)
- `SIMPLE_JWT` (configuração de tokens JWT)
- `SWAGGER_SETTINGS` (documentação da API)

### `database.py`

Configuração do PostgreSQL:

- `DATABASES`
- Variáveis de conexão com o banco

### `cache.py`

Sistema de cache:

- `CACHES` (LocMemCache)
- `CACHE_TIMEOUT`, `CACHE_TIMEOUT_SHORT`

### `email.py`

Sistema de e-mail:

- `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`
- `EMAIL_USE_TLS`, `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`

### `security.py`

Segurança e autenticação:

- `SECRET_KEY`, `DEBUG`, `PRODUCTION`
- `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`
- `AUTH_USER_MODEL`, `AUTH_PASSWORD_VALIDATORS`
- `LOGIN_URL`

### `internationalization.py`

Internacionalização:

- `LANGUAGE_CODE`, `TIME_ZONE`
- `USE_I18N`, `USE_TZ`
- `DATE_FORMAT`

### `static.py`

Arquivos estáticos:

- `STATIC_URL`, `STATIC_ROOT`
- `MEDIA_URL`, `MEDIA_ROOT`

## Como Funciona

1. Django importa `settings/__init__.py`
2. `__init__.py` importa `env.py`
3. `env.py` carrega variáveis de ambiente e importa:
   - `base.py` (que importa apps, rest_framework, cache, i18n, static)
   - `security.py`
   - `database.py`
   - `email.py`

## Vantagens

✅ **Organização**: Cada módulo tem uma responsabilidade clara
✅ **Manutenibilidade**: Fácil localizar e modificar configurações específicas
✅ **Escalabilidade**: Fácil adicionar novos módulos (ex: `celery.py`, `logging.py`)
✅ **Reutilização**: Módulos podem ser reutilizados em outros projetos
✅ **Testabilidade**: Facilita testes isolados de configurações
✅ **Django 6**: Estrutura moderna e alinhada com boas práticas

## Adicionando Novas Configurações

Para adicionar novas configurações, crie um novo arquivo na pasta `settings/` e importe-o em `base.py` ou `env.py`:

```python
# settings/celery.py
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
# ...

# settings/base.py (ou env.py)
from armoreddjango.settings.celery import *
```
