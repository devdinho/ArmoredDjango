# 📧 Melhorias no Sistema de Emails - ArmoredDjango

## 📋 Resumo das Implementações

Este documento descreve as melhorias implementadas no sistema de emails do ArmoredDjango, baseadas nas melhores práticas do projeto Portal CIEGES.

## ✨ Novas Funcionalidades

### 1. Sistema de Email Multipart

**O que mudou:**

- Migração de `EmailMessage` para `EmailMultiAlternatives`
- Emails agora incluem versão texto plano + HTML
- Melhor compatibilidade com clientes de email modernos e antigos

**Por que é melhor:**

- Clientes que não suportam HTML recebem texto plano
- Melhor deliverability (menos chance de cair em spam)
- Segue RFC 2046 para emails multipart

### 2. Template HTML Profissional

**Arquivo:** [`service/src/utils/email_template.html`](service/src/utils/email_template.html)

**Características:**

- Design responsivo e profissional
- CSS inline automático (via Pynliner)
- Compatível com principais clientes de email
- Estrutura modular (header, body, footer)

**Como usar:**

```python
from utils.emails import build_email_html

html = build_email_html(
    title="Título do Email",
    header_content="<h1>Cabeçalho</h1>",
    body_content="<p>Conteúdo principal</p>",
    footer_content="© Seu texto de rodapé",
)
```

### 3. Nova Função de Notificação Genérica

**Função:** `send_notification_email()`

**Uso:**

```python
from utils.emails import send_notification_email

send_notification_email(
    user=user,
    notification_title="Nova Mensagem",
    notification_message="Você recebeu uma nova mensagem no sistema.",
    action_url="https://example.com/messages/123",
    action_label="Ver Mensagem",
)
```

**Benefícios:**

- Reutilizável para qualquer tipo de notificação
- Suporte a botões de ação
- Template consistente com o resto do sistema

### 4. Funções de Validação e Formatação

**Arquivo:** [`service/src/utils/useful_functions.py`](service/src/utils/useful_functions.py)

#### 4.1 Validação de CPF

```python
from utils.useful_functions import validate_cpf, format_cpf

# Validar CPF
cpf = validate_cpf("12345678909")  # Retorna CPF se válido, lança ValidationError se inválido

# Formatar CPF
cpf_formatted = format_cpf("12345678909")  # Retorna "123.456.789-09"
```

#### 4.2 Validação de Telefone

```python
from utils.useful_functions import validate_phone, format_phone

# Validar telefone
phone = validate_phone("11999887766")  # Retorna telefone se válido

# Formatar telefone
phone_formatted = format_phone("11999887766")  # Retorna "(11) 99988-7766"
```

#### 4.3 Sanitização de Strings

```python
from utils.useful_functions import sanitize_string

# Limpar espaços extras
clean_text = sanitize_string("  Hello   World  ")  # Retorna "Hello World"

# Com limite de tamanho
short_text = sanitize_string("Very long text", max_length=10)  # Retorna "Very long "
```

### 5. Headers de Email Aprimorados

**Novos headers adicionados:**

```python
{
    "Message-ID": "<uuid7>@domain.com",      # Rastreamento único
    "X-Mailer": "ArmoredDjango/1.0",         # Identificação do sistema
    "X-Priority": "3",                       # Prioridade normal
    "X-Entity-Ref-ID": "<uuid7>",           # Referência da entidade
}
```

**Benefícios:**

- Melhor rastreamento de emails
- Facilita threading e conversações
- Identificação clara do remetente

### 6. Emails de Boas-Vindas e Reset Aprimorados

#### Email de Boas-Vindas

```python
from utils.emails import send_welcome_email

# Simples
send_welcome_email(user)

# Com mensagem customizada
send_welcome_email(
    user,
    custom_message="Aproveite nossa promoção de boas-vindas!"
)
```

**Melhorias:**

- Template HTML profissional
- Suporte a mensagens customizadas
- Design moderno e responsivo

#### Email de Reset de Senha

```python
from utils.emails import send_password_reset_email

send_password_reset_email(user, reset_url="https://example.com/reset/token")
```

**Melhorias:**

- Box de alerta de segurança destacado
- Botão de ação visível
- Instruções claras
- Aviso sobre segurança

## 🧪 Testes Completos

### Testes de Email

**Arquivo:** [`service/src/utils/tests/test_emails.py`](service/src/utils/tests/test_emails.py)

**Cobertura:**

- ✅ Envio de email texto plano
- ✅ Envio de email multipart (texto + HTML)
- ✅ Headers customizados
- ✅ Email de boas-vindas
- ✅ Email de reset de senha
- ✅ Email de notificação
- ✅ BCC e Reply-To
- ✅ Carregamento de template
- ✅ Construção de HTML

### Testes de Validação

**Arquivo:** [`service/src/utils/tests/test_useful_functions.py`](service/src/utils/tests/test_useful_functions.py)

**Cobertura:**

- ✅ Validação de CPF válido e inválido
- ✅ Formatação de CPF
- ✅ Validação de telefone (celular e fixo)
- ✅ Formatação de telefone
- ✅ Sanitização de strings
- ✅ Casos de erro e exceções

## 🚀 Como Executar os Testes

### Com Docker

```bash
docker compose run test
```

### Localmente

```bash
cd service/src
pytest utils/tests/test_emails.py -v
pytest utils/tests/test_useful_functions.py -v
```

## 📊 Comparação: Antes vs Depois

### Sistema de Email

| Aspecto             | Antes                           | Depois                                |
| ------------------- | ------------------------------- | ------------------------------------- |
| **Tipo de Email**   | EmailMessage (só HTML ou texto) | EmailMultiAlternatives (texto + HTML) |
| **Template**        | HTML inline básico              | Template reutilizável profissional    |
| **Headers**         | Básicos                         | Completos com rastreamento            |
| **Notificações**    | Não existia                     | Função genérica reutilizável          |
| **Compatibilidade** | Apenas clientes modernos        | Todos os clientes                     |

### Funções Úteis

| Funcionalidade         | Antes          | Depois                     |
| ---------------------- | -------------- | -------------------------- |
| **Validação CPF**      | ❌ Não existia | ✅ Completa com formatação |
| **Validação Telefone** | ❌ Não existia | ✅ Celular e fixo          |
| **Sanitização**        | ❌ Não existia | ✅ Com limite de tamanho   |
| **Testes**             | ❌ Não existia | ✅ 30+ testes              |

## 📝 Exemplos de Uso

### Exemplo 1: Email de Notificação de Pagamento

```python
from django.contrib.auth import get_user_model
from utils.emails import send_notification_email

User = get_user_model()
user = User.objects.get(username="john.doe")

send_notification_email(
    user=user,
    notification_title="Pagamento Aprovado",
    notification_message="Seu pagamento de R$ 150,00 foi aprovado com sucesso!",
    action_url="https://example.com/payments/invoice/123",
    action_label="Ver Comprovante",
)
```

### Exemplo 2: Validação de CPF em Formulário

```python
from django import forms
from utils.useful_functions import validate_cpf

class UserForm(forms.Form):
    cpf = forms.CharField(max_length=14)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        try:
            return validate_cpf(cpf)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
```

### Exemplo 3: Email Customizado com Template

```python
from utils.emails import build_email_html, send_email

header = '<h1 style="color: #00529C;">Minha Empresa</h1>'
body = '''
    <p>Olá <strong>João</strong>,</p>
    <p>Este é um email customizado.</p>
    <a href="https://example.com" class="button">Clique Aqui</a>
'''

html = build_email_html(
    title="Email Customizado",
    header_content=header,
    body_content=body,
)

send_email(
    subject="Assunto do Email",
    text_content="Versão texto plano",
    recipient_list=["user@example.com"],
    html_content=html,
)
```

## 🔧 Configuração

### Variáveis de Ambiente (`.env`)

```bash
# Configuração de Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Testando Email Localmente

Para testar sem enviar emails reais:

```python
# settings.py ou .env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Emails serão exibidos no console ao invés de serem enviados.

## 📚 Referências

- **RFC 2046**: Multipart Media Types
- **RFC 5322**: Internet Message Format
- **Pynliner**: CSS Inliner para emails
- **Django EmailMultiAlternatives**: Documentação oficial

## 🎯 Próximos Passos Sugeridos

1. **Adicionar templates de email específicos do seu negócio**

   - Confirmação de pedido
   - Nota fiscal
   - etc.

2. **Implementar sistema de queue para emails**

   - Celery para envio assíncrono
   - Retry automático em caso de falha

3. **Analytics de emails**

   - Rastreamento de abertura (tracking pixel)
   - Rastreamento de cliques

4. **Mais validações**
   - CNPJ
   - CEP
   - Email
   - Cartão de crédito (com mascaramento)

## 🤝 Contribuindo

Se você adicionar novas funcionalidades:

1. ✅ Adicione testes unitários
2. ✅ Documente no código
3. ✅ Atualize este README
4. ✅ Execute `black`, `isort` e `flake8`

## 📄 Licença

As implementações seguem a mesma licença MIT do ArmoredDjango.

---

**Desenvolvido com base nas melhores práticas do Portal CIEGES** 🚀
