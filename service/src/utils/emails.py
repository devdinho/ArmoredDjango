"""
Email utility functions for sending emails.
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from pynliner import Pynliner


def send_email(
    subject: str,
    text_content: str,
    recipient_list: list,
    html_content: str = None,
    from_email: str = None,
    inline_css: bool = True,
) -> bool:
    """
    Envia um email com suporte a conteúdo HTML.

    Args:
        subject (str): Assunto do email
        text_content (str): Conteúdo em texto plano
        recipient_list (list): Lista de destinatários
        html_content (str, optional): Conteúdo HTML do email
        from_email (str, optional): Email do remetente. Se None, usa DEFAULT_FROM_EMAIL
        inline_css (bool, optional): Se True, converte CSS externo em inline styles. Default: True

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> send_email(
        ...     subject="Bem-vindo!",
        ...     text_content="Bem-vindo ao nosso sistema.",
        ...     recipient_list=["user@example.com"],
        ...     html_content="<h1>Bem-vindo ao nosso sistema!</h1>"
        ... )
        True
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)

        if html_content:
            # Converte CSS externo em inline styles para melhor compatibilidade
            if inline_css:
                try:
                    html_content = Pynliner().from_string(html_content).run()
                except Exception as e:
                    print(f"Erro ao aplicar CSS inline: {e}")
                    # Continua sem inline CSS se falhar

            msg.attach_alternative(html_content, "text/html")

        msg.send()
        return True

    except Exception as e:
        # Log the error in production
        print(f"Erro ao enviar email: {e}")
        return False


def send_welcome_email(user) -> bool:
    """
    Envia um email de boas-vindas ao usuário.

    Args:
        user: Objeto do usuário (Profile)

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> from django.contrib.auth import get_user_model
        >>> User = get_user_model()
        >>> user = User.objects.get(username="john.doe")
        >>> send_welcome_email(user)
        True
    """
    subject = "Bem-vindo ao Sistema!"

    text_content = f"""
    Olá {user.get_full_name() or user.username},

    Seja bem-vindo ao nosso sistema!

    Seu cadastro foi realizado com sucesso.

    Atenciosamente,
    Equipe do Sistema
    """

    html_content = f"""
    <html>
        <body>
            <h2>Olá {user.get_full_name() or user.username},</h2>
            <p>Seja bem-vindo ao nosso sistema!</p>
            <p>Seu cadastro foi realizado com sucesso.</p>
            <br>
            <p>Atenciosamente,<br>
            Equipe do Sistema</p>
        </body>
    </html>
    """

    return send_email(
        subject=subject,
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


def send_password_reset_email(user, reset_url: str) -> bool:
    """
    Envia um email de redefinição de senha ao usuário.

    Args:
        user: Objeto do usuário (Profile)
        reset_url (str): URL para redefinição de senha

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> send_password_reset_email(user, "https://example.com/reset/token123")
        True
    """
    subject = "Redefinição de Senha"

    text_content = f"""
    Olá {user.get_full_name() or user.username},

    Recebemos uma solicitação para redefinir sua senha.

    Para redefinir sua senha, acesse o link abaixo:
    {reset_url}

    Se você não solicitou esta redefinição, ignore este email.

    Atenciosamente,
    Equipe do Sistema
    """

    html_content = f"""
    <html>
        <body>
            <h2>Olá {user.get_full_name() or user.username},</h2>
            <p>Recebemos uma solicitação para redefinir sua senha.</p>
            <p>Para redefinir sua senha, clique no botão abaixo:</p>
            <p>
                <a href="{reset_url}"
                   style="background-color: #4CAF50;
                          color: white;
                          padding: 10px 20px;
                          text-decoration: none;
                          border-radius: 5px;
                          display: inline-block;">
                    Redefinir Senha
                </a>
            </p>
            <p>Ou copie e cole o link abaixo no seu navegador:</p>
            <p>{reset_url}</p>
            <br>
            <p><small>Se você não solicitou esta redefinição, ignore este email.</small></p>
            <br>
            <p>Atenciosamente,<br>
            Equipe do Sistema</p>
        </body>
    </html>
    """

    return send_email(
        subject=subject,
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )
