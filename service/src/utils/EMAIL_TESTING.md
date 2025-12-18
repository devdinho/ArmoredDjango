# 🧪 Como Testar o Envio de Emails

## ⚡ Método Rápido (Recomendado)

### Usando Comando Django

```bash
# Testar todos os tipos de email
python manage.py test_email seu-email@gmail.com

# Testar apenas um tipo
python manage.py test_email seu-email@gmail.com --tipo=cadastro
python manage.py test_email seu-email@gmail.com --tipo=recuperacao
python manage.py test_email seu-email@gmail.com --tipo=notificacao
python manage.py test_email seu-email@gmail.com --tipo=pagamento

# Usar um usuário específico
python manage.py test_email seu-email@gmail.com --username=admin
```

**Exemplo de saída:**

```
============================================================
🧪 TESTE DE ENVIO DE EMAILS
============================================================

✅ Usuário: admin (admin@example.com)
📧 Destino: seu-email@gmail.com

------------------------------------------------------------
1️⃣  Email de Cadastro/Boas-Vindas
------------------------------------------------------------
   ✅ Enviado com sucesso!

------------------------------------------------------------
2️⃣  Email de Recuperação de Senha
------------------------------------------------------------
   ✅ Enviado com sucesso!

============================================================
📊 RESUMO
============================================================

  ✅ Cadastro
  ✅ Recuperação
  ✅ Notificação
  ✅ Pagamento

  Total: 4 | Sucesso: 4 | Falhas: 0

------------------------------------------------------------
📬 Verifique sua caixa de entrada: seu-email@gmail.com
============================================================
```

---

## 📝 Método Alternativo

### Usando Script Python

1. **Edite o arquivo de teste:**

```bash
nano service/src/utils/test_send_email.py
```

2. **Altere o email de destino:**

```python
# No início do arquivo
EMAIL_TESTE = "seu-email@gmail.com"  # ALTERE AQUI!
```

3. **Execute:**

```bash
cd service/src
python manage.py shell < utils/test_send_email.py
```

---

## 🐚 Método Manual (Shell Interativo)

```bash
cd service/src
python manage.py shell
```

```python
# No shell Python
from django.contrib.auth import get_user_model
from utils.email_examples import exemplo_email_cadastro_simples

User = get_user_model()
user = User.objects.first()

# Temporariamente muda o email do usuário
user.email = "seu-email@gmail.com"

# Envia email de teste
exemplo_email_cadastro_simples(user)
```

---

## ⚙️ Configuração de Email

### Para Gmail

No seu arquivo `.env`:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

**📌 Importante:** Use uma [senha de app](https://support.google.com/accounts/answer/185833), não sua senha normal!

### Para Desenvolvimento (Console)

Se quiser apenas ver os emails no console sem enviar:

```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Os emails aparecerão no terminal onde o Django está rodando.

### Para Desenvolvimento (Arquivo)

Se quiser salvar os emails em arquivos:

```bash
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
EMAIL_FILE_PATH=/tmp/app-emails
```

---

## 🔍 Testando Tipos Específicos

### 1. Email de Cadastro

```bash
python manage.py test_email seu-email@gmail.com --tipo=cadastro
```

### 2. Email de Recuperação de Senha

```bash
python manage.py test_email seu-email@gmail.com --tipo=recuperacao
```

### 3. Email de Notificação

```bash
python manage.py test_email seu-email@gmail.com --tipo=notificacao
```

### 4. Email de Pagamento

```bash
python manage.py test_email seu-email@gmail.com --tipo=pagamento
```

---

## 🐳 Testando com Docker

```bash
# Entre no container
docker exec -it armoreddjango_service bash

# Execute o comando de teste
python src/manage.py test_email seu-email@gmail.com
```

---

## ❓ Troubleshooting

### Não recebeu o email?

1. **Verifique as configurações SMTP no `.env`**

   ```bash
   cat .env | grep EMAIL
   ```

2. **Verifique a pasta de spam**

   - Emails podem ser marcados como spam na primeira vez

3. **Teste com console backend primeiro**
   ```bash
   # .env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
4. **Verifique os logs**

   ```bash
   # Docker
   docker logs armoreddjango_service

   # Local
   python manage.py runserver
   ```

### Erro de autenticação SMTP?

- **Gmail:** Precisa de senha de app (não a senha normal)
- **Outros:** Verifique se SMTP está habilitado

### Erro de SSL/TLS?

```bash
# Para Gmail use TLS
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# Para outros provedores que usam SSL
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

---

## 💡 Dicas

### Testar com Email Temporário

Use serviços como:

- [Mailtrap](https://mailtrap.io) - Email testing
- [MailHog](https://github.com/mailhog/MailHog) - Local SMTP server
- [Temp-Mail](https://temp-mail.org) - Email descartável

### Configuração Mailtrap (Recomendado para Dev)

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-usuario-mailtrap
EMAIL_HOST_PASSWORD=sua-senha-mailtrap
```

---

## 📚 Mais Informações

- **Exemplos de Código**: [`email_examples.py`](email_examples.py)
- **Guia Rápido**: [`EMAIL_QUICK_START.md`](EMAIL_QUICK_START.md)
- **Documentação**: [`EMAIL_IMPROVEMENTS.md`](EMAIL_IMPROVEMENTS.md)

---

## 🎯 Resumo Rápido

```bash
# Método mais fácil
python manage.py test_email seu-email@gmail.com

# Só um tipo
python manage.py test_email seu-email@gmail.com --tipo=cadastro

# Com Docker
docker exec -it armoreddjango_service python src/manage.py test_email seu-email@gmail.com
```

**Pronto! 🚀**
