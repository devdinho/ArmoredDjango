![ArmoredDjango](title.png)

# 🛡️ ArmoredDjango

**Template Django profissional e pronto para produção** com autenticação JWT, gerenciamento de usuários, validação de senhas complexas, sistema de emails, cache, testes completos e integração Docker.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/) [![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Sumário

- [Visão Geral](#-visão-geral)
- [Usar como Template](#-usar-como-template)
- [Features](#-features)
- [Tecnologias](#-tecnologias)
- [Requisitos](#-requisitos)
- [Instalação Rápida](#-instalação-rápida)
- [Configuração](#-configuração)
- [Executando o Projeto](#-executando-o-projeto)
- [Testes](#-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Deploy](#-deploy)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

**ArmoredDjango** é um template Django completo e pronto para produção, ideal para iniciar novos projetos rapidamente. Elimina a necessidade de configurações repetitivas e implementa as melhores práticas da comunidade Django.

### Para quem é este template?

- ✅ Desenvolvedores que querem iniciar projetos Django rapidamente
- ✅ Equipes que buscam um boilerplate com melhores práticas
- ✅ Projetos que precisam de autenticação JWT desde o início
- ✅ Aplicações que exigem controle granular de permissões

---

## 🎨 Usar como Template

### Renomear o Projeto

Este template inclui scripts para renomear facilmente o projeto para o seu próprio nome:

#### **Opção 1: Script Python (Recomendado)**

```bash
# Renomeia o projeto para "myproject"
python rename_project.py myproject
```

#### **Opção 2: Script Bash**

```bash
# Torna o script executável (primeira vez)
chmod +x rename_project.sh

# Renomeia o projeto
./rename_project.sh myproject
```

### O que os scripts fazem?

✅ Renomeiam o diretório principal do app  
✅ Atualizam todas as referências no código  
✅ Atualizam `docker-compose.yaml`  
✅ Atualizam `pyproject.toml`  
✅ Atualizam configurações do Django  
✅ Atualizam scripts de inicialização

### Após renomear:

```bash
# 1. Reconstruir containers
docker compose build

# 2. Iniciar o projeto
docker compose up -d

# 3. Verificar se está funcionando
docker logs armoreddjango_service
```

---

## ✨ Features

### 🔐 Autenticação & Segurança

- ✅ Autenticação JWT (Simple JWT)
- ✅ Modelo de usuário customizado (`Profile`)
- ✅ Validação de senha complexa (maiúscula, minúscula, número, caractere especial)
- ✅ Senha mínima de 8 caracteres
- ✅ Sistema de permissões e grupos
- ✅ Histórico de alterações (django-simple-history)
- ✅ Rate limiting (5/s anônimo, 20/s autenticado)

### 🎨 Painel Administrativo

- ✅ MaterialDash - Interface admin moderna e responsiva
- ✅ Theme Material Design
- ✅ Dashboard intuitivo e profissional
- ✅ Melhor experiência de gerenciamento

### 📧 Sistema de Emails

- ✅ **Emails multipart** (texto + HTML) com EmailMultiAlternatives
- ✅ **Template HTML profissional** responsivo e modular
- ✅ **9 tipos de emails prontos**: cadastro, recuperação de senha, notificações, pagamentos, etc
- ✅ **Validação brasileira**: CPF e telefone com formatação automática
- ✅ **CSS inline automático** (Pynliner) para compatibilidade
- ✅ **Comando de teste**: `python manage.py test_email seu-email@example.com`
- ✅ **Documentação completa**: guia rápido, exemplos e troubleshooting

### 🚀 Performance & Cache

- ✅ Sistema de cache configurado
- ✅ Timeouts de cache configuráveis (1 hora / 5 minutos)
- ✅ Exemplo de função de cache incluído

### 🧪 Testes

- ✅ **80+ testes unitários** incluídos
- ✅ Pytest configurado
- ✅ Cobertura de models, serializers, validators, emails e funções úteis
- ✅ Scripts prontos para CI/CD
- ✅ Testes de email com backend locmem

### 🐳 Docker & DevOps

- ✅ Docker Compose completo
- ✅ Dockerfile otimizado com Poetry
- ✅ Scripts de inicialização automática
- ✅ Configurações separadas para dev/prod
- ✅ GitHub Actions workflow incluído

### 📚 Documentação

- ✅ Swagger/OpenAPI integrado
- ✅ ReDoc disponível
- ✅ Código bem documentado
- ✅ Type hints em Python

---

## 🛠️ Tecnologias

### Backend

- **Django 6.0** - Framework web
- **Django REST Framework 3.15.2** - API REST
- **djangorestframework-simplejwt 5.5.1** - Autenticação JWT
- **PostgreSQL 17** - Banco de dados
- **Gunicorn 23.x** - Servidor WSGI para produção
- **MaterialDash 0.0.24.2+** - Interface admin moderna

### DevOps & Tools

- **Docker & Docker Compose** - Containerização
- **Poetry** - Gerenciamento de dependências
- **Pytest 8.3.5+** - Framework de testes
- **pytest-django 4.11.1+** - Integração Django/Pytest
- **GitHub Actions** - CI/CD

### Bibliotecas Adicionais

- **django-cors-headers 4.7.0+** - CORS
- **drf-yasg 1.21.11+** - Documentação Swagger/OpenAPI
- **django-simple-history 3.8.0** - Auditoria e histórico de mudanças
- **Pillow 12.0+** - Processamento de imagens
- **Pynliner 0.8.0+** - CSS inline para emails
- **Bleach 4.1.0** - Sanitização de HTML
- **python-slugify 8.0.4+** - Geração de slugs
- **python-dotenv 1.0.1** - Variáveis de ambiente
- **Requests 2.32.3+** - Cliente HTTP
- **psycopg2-binary 2.9.10** - Adaptador PostgreSQL

---

## 📦 Requisitos

- **Python 3.12+**
- **Docker & Docker Compose** (recomendado)
- **PostgreSQL 17** (se não usar Docker)
- **Poetry** (opcional, para instalação local)

---

## 🚀 Instalação Rápida

### Com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/devdinho/ArmoredDjango.git
cd ArmoredDjango

# 2. Copie o arquivo de exemplo e configure as variáveis
cp .env.example .env

# 3. Edite o .env e configure suas variáveis
nano .env  # ou seu editor preferido

# 4. Suba os containers
docker compose up --build

# 5. Acesse a aplicação
# http://localhost:8003/
# http://localhost:8003/admin/
# http://localhost:8003/swagger/
```

### Instalação Local (Sem Docker)

```bash
# 1. Clone o repositório
git clone https://github.com/devdinho/ArmoredDjango.git
cd ArmoredDjango

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instale as dependências
cd service
poetry install
# ou
pip install -r requirements.txt

# 4. Configure o .env
cp ../.env.example ../.env
nano ../.env

# 5. Execute as migrações
python src/manage.py migrate

# 6. Crie um superusuário
python src/manage.py createsuperuser

# 7. Inicie o servidor
python src/manage.py runserver 0.0.0.0:8003
```

---

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
PRODUCTION=False

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432

# Admin
ADMIN_PASSWORD=admin123!

# System
SYSTEM_URL=localhost

# CORS
CORS_ALLOW_ALL_ORIGINS=False

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

### 2. Gerando SECRET_KEY

O Django precisa de uma `SECRET_KEY` segura. Para gerar uma nova:

**Método 1: Usando Django (recomendado)**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Método 2: Usando Python puro**

```python
import secrets
print(secrets.token_urlsafe(50))
```

⚠️ **IMPORTANTE**: Nunca commite sua `SECRET_KEY` no repositório! Mantenha-a sempre no `.env`.

### 3. Configurações de Email

Para usar o sistema de emails, configure seu provedor SMTP no `.env`. Exemplos:

**Gmail:**

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app  # Use senha de app, não sua senha normal
```

**SendGrid:**

```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=sua-api-key
```

**Para Desenvolvimento (Console):**

```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

📚 **Documentação completa do sistema de emails:**

- [Guia Rápido](service/src/utils/EMAIL_QUICK_START.md)
- [Documentação Completa](service/src/utils/EMAIL_IMPROVEMENTS.md)
- [Guia de Testes](service/src/utils/EMAIL_TESTING.md)

---

## 🏃 Executando o Projeto

### Com Docker

```bash

# Build
docker compose up --build

# Logs
docker compose logs -f django

# Parar containers
docker compose down
```

### Localmente

```bash
cd service

# Desenvolvimento
python src/manage.py runserver 0.0.0.0:8003

# Produção (com Gunicorn)
gunicorn -c src/gunicorn_config.py armoreddjango.wsgi:application
```

### Acessando a Aplicação

- **API**: http://localhost:8003/
- **Admin**: http://localhost:8003/admin/
- **Swagger**: http://localhost:8003/swagger/
- **ReDoc**: http://localhost:8003/redoc/

---

## 🧪 Testes

### Executar todos os testes

```bash
# Com Docker
docker compose run test

# Localmente
cd service
./scripts/run_unit_tests.sh
# ou
pytest src/
```

### Executar testes específicos

```bash
# Testes de autenticação
pytest src/authentication/tests/

# Testes de emails
pytest src/utils/tests/test_emails.py

# Testes de validação (CPF/telefone)
pytest src/utils/tests/test_useful_functions.py

# Testes de um arquivo específico
pytest src/authentication/tests/test_validators.py

# Testes com coverage
pytest --cov=src --cov-report=html
```

### Testar envio de emails

```bash
# Enviar emails de teste para seu email
python manage.py test_email seu-email@example.com

# Testar tipo específico
python manage.py test_email seu-email@example.com --tipo=cadastro

# Com Docker
docker exec -it armoreddjango_service python src/manage.py test_email seu-email@example.com
```

📚 Veja o [Guia de Testes de Email](service/src/utils/EMAIL_TESTING.md) para mais detalhes.

### Lint & Formatação

```bash
# Com Docker
docker compose run lint

# Localmente
cd service
./scripts/start-lint.sh src

# Ou manualmente
black src/
isort src/
flake8 src/
```

---

## 📁 Estrutura do Projeto

```
armoreddjango/
├── .github/
│   └── workflows/
│       └── lint-and-test.yml      # CI/CD workflow
├── service/
│   ├── Dockerfile                  # Container configuration
│   ├── pyproject.toml             # Dependencies
│   ├── scripts/
│   │   ├── start.sh               # Startup script
│   │   ├── start-lint.sh          # Linting script
│   │   └── run_unit_tests.sh      # Test script
│   └── src/
│       ├── manage.py              # Django management
│       ├── gunicorn_config.py     # Gunicorn config
│       ├── armoreddjango/         # Main project
│       │   ├── settings/
│       │   │   ├── base.py        # Base settings
│       │   │   └── env.py         # Environment settings
│       │   ├── urls.py            # URL configuration
│       │   ├── asgi.py
│       │   └── wsgi.py
│       ├── authentication/        # Authentication app
│       │   ├── models/
│       │   │   ├── Profile.py     # User model
│       │   │   └── Groups.py
│       │   ├── serializers/
│       │   │   └── ProfileSerializer.py
│       │   ├── api/
│       │   │   ├── ProfileRestView.py
│       │   │   └── CreateProfileRestView.py
│       │   ├── admin/
│       │   │   ├── ProfileAdmin.py
│       │   │   └── GroupsAdmin.py
│       │   ├── validators.py      # Password validators
│       │   └── tests/             # 50+ tests
│       │       ├── test_validators.py
│       │       ├── test_profile_model.py
│       │       └── test_serializers.py
│       └── utils/                 # Utilities
│           ├── constants.py       # Constants
│           ├── cache_utils.py     # Cache helpers
│           ├── emails.py          # Email functions
│           ├── email_template.html # Email HTML template
│           ├── email_examples.py  # 9 email examples
│           ├── useful_functions.py # CPF/phone validation
│           ├── management/        # Django commands
│           │   └── commands/
│           │       └── test_email.py # Email test command
│           ├── tests/
│           │   ├── test_emails.py # Email tests
│           │   └── test_useful_functions.py # Validation tests
│           ├── EMAIL_QUICK_START.md # Quick start guide
│           ├── EMAIL_IMPROVEMENTS.md # Full documentation
│           └── EMAIL_TESTING.md   # Testing guide
├── docker-compose.yaml            # Docker Compose
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## 🔌 API Endpoints

### Autenticação

```
POST   /api/login/           # Obter token JWT
POST   /api/login/refresh/   # Refresh token
POST   /api/login/verify/    # Verificar token
POST   /api/logout/          # Blacklist token
```

### Perfis de Usuário

```
POST   /api/register         # Criar novo usuário
GET    /api/profile          # Listar usuários
GET    /api/profile/{id}     # Obter usuário específico
PUT    /api/profile/{id}     # Atualizar usuário
PATCH  /api/profile/{id}     # Atualizar parcialmente
```

### Documentação

```
GET    /swagger/             # Swagger UI
GET    /redoc/               # ReDoc UI
GET    /admin/               # Django Admin
```

### Exemplo de Uso

```bash
# Criar usuário
curl -X POST http://localhost:8003/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123!"
  }'

# Login
curl -X POST http://localhost:8003/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.doe",
    "password": "SecurePass123!"
  }'

# Usar token
curl -X GET http://localhost:8003/api/profile \
  -H "Authorization: Bearer seu-token-jwt-aqui"
```

---

## ⚙️ Configurações do Gunicorn

O projeto inclui 3 configurações prontas para diferentes cenários de uso. Escolha a mais adequada ao seu caso:

### 1️⃣ API Simples (CRUD, REST) - **Padrão**

```python
# service/src/gunicorn_config.py
# Bom equilíbrio para APIs tradicionais
# Requests curtas, pouco processamento pesado

workers = 4          # Escala bem em máquinas com 2–4 vCPUs
threads = 2          # Pequeno ganho em I/O (DB, cache)
timeout = 30         # Padrão seguro

bind = "0.0.0.0:8003"
chdir = "/app/"
module = "armoreddjango.wsgi:application"
```

**Quando usar:** CRUD tradicional, APIs REST, sem conexões longas.

### 2️⃣ API com SSE / Streaming

```python
# Ideal para Server-Sent Events ou conexões longas
# Poucos workers para não travar novas conexões

workers = 2          # Poucos processos para evitar bloqueio
threads = 8          # Cada thread pode segurar um stream
timeout = 0          # Nunca matar conexão SSE

bind = "0.0.0.0:8003"
chdir = "/app/"
module = "armoreddjango.wsgi:application"
```

**Quando usar:** Server-Sent Events, streaming de dados, conexões persistentes.

### 3️⃣ API com LLM (Streaming de IA)

```python
# Configuração para LLMs (OpenAI, Anthropic, etc)
# Requests longas, I/O bound, streaming contínuo

workers = 1          # LLM consome muita memória
threads = 12         # Suporta múltiplas streams simultâneas
timeout = 0          # Streaming nunca deve expirar

bind = "0.0.0.0:8003"
chdir = "/app/"
module = "armoreddjango.wsgi:application"
```

**Quando usar:** Integração com LLMs, streaming de respostas de IA, processamento pesado.

### 📊 Resumo Rápido

| Cenário           | Workers | Threads | Timeout | Uso               |
| ----------------- | ------- | ------- | ------- | ----------------- |
| **CRUD/REST**     | 4       | 2       | 30s     | APIs tradicionais |
| **SSE/Streaming** | 2       | 8       | 0       | Conexões longas   |
| **LLM/IA**        | 1       | 12      | 0       | Streaming de IA   |

### 💡 Conceitos

- **Workers:** Processos separados (CPU-bound, mais memória)
- **Threads:** Mais leves (I/O-bound, compartilham memória)
- **Timeout:** Tempo máximo de resposta (0 = sem limite)

**Dica:** Comece com a configuração padrão e ajuste conforme a necessidade.

---

## 🚀 Deploy

### Preparação

1. Configure `PRODUCTION=True` no `.env`
2. Defina `DEBUG=False`
3. Configure `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`
4. Gere uma nova `SECRET_KEY` segura
5. Configure email SMTP de produção
6. Configure backup do banco de dados
7. **Escolha a configuração adequada do Gunicorn** (veja seção acima)

### Docker em Produção

```bash
docker compose up --build -d
```

### Coleta de Arquivos Estáticos

```bash
python src/manage.py collectstatic --noinput
```

### Checklist de Segurança

- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` única e segura
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS configurado (Let's Encrypt, Cloudflare, etc)
- [ ] Firewall configurado (apenas portas necessárias)
- [ ] Backup automático do banco de dados
- [ ] Logs configurados e monitorados
- [ ] Rate limiting ativado

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estas etapas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git switch -c feat/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feat/nova-feature`)
5. Abra um Pull Request

### Diretrizes

- ✅ Siga o estilo de código (Black, isort, Flake8)
- ✅ Adicione testes para novas features
- ✅ Atualize a documentação
- ✅ Mantenha commits claros e descritivos

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Anderson Freitas**

- Email: freitas.dev@proton.me
- GitHub: [@devdinho](https://github.com/devdinho)

---

## 🙏 Agradecimentos

- Comunidade Django
- Equipe Django REST Framework
- Todos os contribuidores de bibliotecas open source utilizadas

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**
