# 📧 Guia Rápido de Uso - Sistema de Emails

## 🚀 Exemplos Prontos para Usar

Todos os exemplos estão em [`email_examples.py`](email_examples.py) - copie e adapte!

## 1️⃣ Email de Cadastro / Boas-Vindas

### Exemplo Simples

```python
from utils.email_examples import exemplo_email_cadastro_simples

# Em sua view de registro
def register_view(request):
    # Após criar o usuário
    user = User.objects.create_user(...)

    # Envia email de boas-vindas
    exemplo_email_cadastro_simples(user)

    return redirect('success')
```

### Com Mensagem Customizada

```python
from utils.email_examples import exemplo_email_cadastro_com_mensagem_customizada

exemplo_email_cadastro_com_mensagem_customizada(user)
```

### Totalmente Customizado

```python
from utils.email_examples import exemplo_email_cadastro_completo_customizado

exemplo_email_cadastro_completo_customizado(user, request)
```

## 2️⃣ Email de Recuperação de Senha

### Exemplo Simples

```python
from utils.email_examples import exemplo_email_recuperacao_senha_simples

# Em sua view de forgot password
def forgot_password_view(request):
    email = request.POST.get('email')
    user = User.objects.get(email=email)

    # Envia email de reset
    exemplo_email_recuperacao_senha_simples(user, request)

    return redirect('password_reset_sent')
```

### Com Informação de Expiração

```python
from utils.email_examples import exemplo_email_recuperacao_senha_com_expiracao

exemplo_email_recuperacao_senha_com_expiracao(user, request, tempo_expiracao="1 hora")
```

## 3️⃣ Email de Notificação

### Notificação Simples

```python
from utils.email_examples import exemplo_notificacao_simples

# Após atualização de perfil
exemplo_notificacao_simples(user)
```

### Notificação com Botão de Ação

```python
from utils.email_examples import exemplo_notificacao_com_acao

# Quando recebe nova mensagem
exemplo_notificacao_com_acao(user)
```

### Notificação de Pagamento

```python
from utils.email_examples import exemplo_notificacao_pagamento_aprovado

# Após confirmar pagamento
exemplo_notificacao_pagamento_aprovado(user, valor=150.00, pedido_id=123)
```

### Alerta de Segurança

```python
from utils.email_examples import exemplo_notificacao_login_novo_dispositivo

# Quando detecta login suspeito
exemplo_notificacao_login_novo_dispositivo(
    user,
    dispositivo="iPhone 13 - Safari",
    localizacao="São Paulo, SP",
    ip="192.168.1.1"
)
```

## 4️⃣ Outros Tipos de Email

### Confirmação de Email

```python
from utils.email_examples import exemplo_email_confirmacao_email

confirmation_url = "https://example.com/confirm/abc123"
exemplo_email_confirmacao_email(user, confirmation_url)
```

### Confirmação de Mudança de Senha

```python
from utils.email_examples import exemplo_email_mudanca_senha_confirmacao

# Após usuário alterar senha
exemplo_email_mudanca_senha_confirmacao(user)
```

### Exclusão de Conta

```python
from utils.email_examples import exemplo_email_exclusao_conta

# Quando usuário solicita exclusão
exemplo_email_exclusao_conta(user, dias_para_exclusao=30)
```

## 📋 Tipos de Emails Disponíveis

| Tipo                     | Quando Usar              | Exemplo                                      |
| ------------------------ | ------------------------ | -------------------------------------------- |
| **Cadastro**             | Após criar conta         | `exemplo_email_cadastro_simples`             |
| **Recuperação de Senha** | Esqueci minha senha      | `exemplo_email_recuperacao_senha_simples`    |
| **Notificação Genérica** | Qualquer notificação     | `exemplo_notificacao_simples`                |
| **Pagamento**            | Confirmação de pagamento | `exemplo_notificacao_pagamento_aprovado`     |
| **Segurança**            | Login suspeito           | `exemplo_notificacao_login_novo_dispositivo` |
| **Confirmação Email**    | Validar email            | `exemplo_email_confirmacao_email`            |
| **Mudança Senha**        | Após alterar senha       | `exemplo_email_mudanca_senha_confirmacao`    |
| **Exclusão Conta**       | Deletar conta            | `exemplo_email_exclusao_conta`               |

## 🔧 Usando com Django Signals

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from utils.email_examples import exemplo_email_cadastro_simples

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email_on_signup(sender, instance, created, **kwargs):
    """Envia email de boas-vindas automaticamente após cadastro."""
    if created:
        exemplo_email_cadastro_simples(instance)
```

## 💡 Dicas

### 1. Testar Emails Localmente

No seu `.env` ou `settings.py`:

```python
# Exibe emails no console (desenvolvimento)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Salva emails em arquivos (desenvolvimento)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-emails'
```

### 2. Envio Assíncrono (Recomendado para Produção)

```python
# tasks.py (Celery)
from celery import shared_task
from utils.email_examples import exemplo_email_cadastro_simples

@shared_task
def send_welcome_email_task(user_id):
    user = User.objects.get(id=user_id)
    exemplo_email_cadastro_simples(user)

# views.py
def register_view(request):
    user = User.objects.create_user(...)

    # Envia email em background
    send_welcome_email_task.delay(user.id)

    return redirect('success')
```

### 3. Personalização

Para criar seu próprio template:

```python
from utils.emails import build_email_html, send_email

# Crie seu conteúdo
header = '<h1>Meu Email</h1>'
body = '<p>Conteúdo personalizado</p>'

# Monta HTML
html = build_email_html(
    title="Título",
    header_content=header,
    body_content=body,
)

# Envia
send_email(
    subject="Assunto",
    text_content="Versão texto",
    recipient_list=["user@example.com"],
    html_content=html,
)
```

## 🧪 Testando

```bash
# Executar testes
cd service/src
pytest utils/tests/test_emails.py -v

# Testar envio real (configure SMTP antes)
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from utils.email_examples import exemplo_email_cadastro_simples
>>> User = get_user_model()
>>> user = User.objects.first()
>>> exemplo_email_cadastro_simples(user)
```

## 📚 Mais Informações

- Documentação completa: [EMAIL_IMPROVEMENTS.md](EMAIL_IMPROVEMENTS.md)
- Todos os exemplos: [email_examples.py](email_examples.py)
- Funções base: [emails.py](emails.py)
- Testes: [tests/test_emails.py](tests/test_emails.py)

## ❓ FAQ

**Q: Posso usar meu próprio template HTML?**  
A: Sim! Use `send_email()` diretamente com seu HTML customizado.

**Q: Como adicionar anexos?**  
A: Use o objeto `EmailMessage` diretamente do Django e o método `.attach()`.

**Q: Os emails funcionam em todos os clientes?**  
A: Sim! Usamos `EmailMultiAlternatives` que envia texto + HTML para máxima compatibilidade.

**Q: Como rastrear se o email foi aberto?**  
A: Adicione um pixel de rastreamento (1x1 transparent gif) no HTML com URL única por email.

---

**🎉 Pronto para usar! Copie os exemplos de [`email_examples.py`](email_examples.py) e adapte para seu projeto.**
