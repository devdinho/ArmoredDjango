"""
Testes para funções de email.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings

from utils.emails import (
    build_email_html,
    load_email_template,
    send_email,
    send_notification_email,
    send_password_reset_email,
    send_welcome_email,
)


@pytest.mark.django_db
class TestEmailFunctions:
    """Testes para funções de envio de email."""

    def setup_method(self):
        """Setup executado antes de cada teste."""
        # Limpa a outbox antes de cada teste
        mail.outbox = []

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_text_only(self):
        """Testa envio de email apenas com texto."""
        result = send_email(
            subject="Test Subject",
            text_content="Test content",
            recipient_list=["test@example.com"],
        )

        assert result is True
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Test Subject"
        assert mail.outbox[0].body == "Test content"
        assert mail.outbox[0].to == ["test@example.com"]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_with_html(self):
        """Testa envio de email com HTML."""
        result = send_email(
            subject="Test Subject",
            text_content="Test content",
            recipient_list=["test@example.com"],
            html_content="<h1>Test HTML</h1>",
        )

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.subject == "Test Subject"
        assert email.body == "Test content"
        assert len(email.alternatives) == 1
        assert "text/html" in email.alternatives[0][1]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_with_headers(self):
        """Testa envio de email com headers customizados."""
        custom_headers = {
            "X-Custom-Header": "Custom Value",
        }

        result = send_email(
            subject="Test Subject",
            text_content="Test content",
            recipient_list=["test@example.com"],
            headers=custom_headers,
        )

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert "X-Custom-Header" in email.extra_headers
        assert email.extra_headers["X-Custom-Header"] == "Custom Value"
        # Verifica headers padrão
        assert "Message-ID" in email.extra_headers
        assert "X-Mailer" in email.extra_headers

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_welcome_email(self):
        """Testa envio de email de boas-vindas."""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="TestPass123!",
        )

        result = send_welcome_email(user)

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert "Bem-vindo" in email.subject
        assert user.get_full_name() in email.body
        assert email.to == [user.email]
        assert len(email.alternatives) == 1  # HTML version

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_welcome_email_with_custom_message(self):
        """Testa envio de email de boas-vindas com mensagem customizada."""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="TestPass123!",
        )

        custom_message = "Esta é uma mensagem customizada."
        result = send_welcome_email(user, custom_message=custom_message)

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert custom_message in email.body

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_password_reset_email(self):
        """Testa envio de email de reset de senha."""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="TestPass123!",
        )

        reset_url = "https://example.com/reset/abc123"
        result = send_password_reset_email(user, reset_url)

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert "Redefinição de Senha" in email.subject
        assert user.get_full_name() in email.body
        assert reset_url in email.body
        assert email.to == [user.email]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_notification_email(self):
        """Testa envio de email de notificação."""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="TestPass123!",
        )

        result = send_notification_email(
            user=user,
            notification_title="Nova Mensagem",
            notification_message="Você recebeu uma nova mensagem.",
            action_url="https://example.com/messages/123",
            action_label="Ver Mensagem",
        )

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert "Nova Mensagem" in email.subject
        assert "nova mensagem" in email.body
        assert email.to == [user.email]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_notification_email_without_action(self):
        """Testa envio de email de notificação sem ação."""
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="TestPass123!",
        )

        result = send_notification_email(
            user=user,
            notification_title="Alerta",
            notification_message="Este é um alerta importante.",
        )

        assert result is True
        assert len(mail.outbox) == 1

    def test_load_email_template(self):
        """Testa carregamento do template de email."""
        template = load_email_template()
        assert template is not None
        assert "{body_content}" in template
        assert "{header_content}" in template
        assert "{footer_content}" in template

    def test_build_email_html(self):
        """Testa construção de HTML do email."""
        html = build_email_html(
            title="Test Email",
            header_content="<h1>Header</h1>",
            body_content="<p>Body</p>",
            footer_content="Footer",
        )

        assert html is not None
        assert "Test Email" in html
        assert "<h1>Header</h1>" in html
        assert "<p>Body</p>" in html
        assert "Footer" in html

    def test_build_email_html_default_footer(self):
        """Testa construção de HTML com footer padrão."""
        html = build_email_html(
            title="Test Email",
            header_content="<h1>Header</h1>",
            body_content="<p>Body</p>",
        )

        assert html is not None
        assert "ArmoredDjango" in html

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_with_bcc(self):
        """Testa envio de email com BCC."""
        result = send_email(
            subject="Test Subject",
            text_content="Test content",
            recipient_list=["test@example.com"],
            bcc=["bcc@example.com"],
        )

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.bcc == ["bcc@example.com"]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_with_reply_to(self):
        """Testa envio de email com Reply-To."""
        result = send_email(
            subject="Test Subject",
            text_content="Test content",
            recipient_list=["test@example.com"],
            reply_to=["reply@example.com"],
        )

        assert result is True
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.reply_to == ["reply@example.com"]

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_multipart(self):
        """Testa que o email é enviado como multipart."""
        result = send_email(
            subject="Test Subject",
            text_content="Plain text version",
            recipient_list=["test@example.com"],
            html_content="<h1>HTML version</h1>",
        )

        assert result is True
        email = mail.outbox[0]
        # Verifica que tanto texto quanto HTML foram incluídos
        assert email.body == "Plain text version"
        assert len(email.alternatives) == 1
        assert "<h1>HTML version</h1>" in email.alternatives[0][0]
