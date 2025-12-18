"""
Email utility functions for sending emails.
"""

import uuid
from pathlib import Path

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
    reply_to: list = None,
    bcc: list = None,
    headers: dict = None,
) -> bool:
    """
    Envia um email multipart (text/plain + text/html) com suporte a clientes modernos.
    
    Esta implementação usa EmailMultiAlternatives para garantir compatibilidade
    com todos os clientes de email, enviando tanto versão texto quanto HTML.

    Args:
        subject (str): Assunto do email
        text_content (str): Conteúdo em texto plano (fallback)
        recipient_list (list): Lista de destinatários
        html_content (str, optional): Conteúdo HTML do email
        from_email (str, optional): Email do remetente. Se None, usa DEFAULT_FROM_EMAIL
        inline_css (bool, optional): Se True, converte CSS externo em inline styles. Default: True
        reply_to (list, optional): Lista de endereços para Reply-To
        bcc (list, optional): Lista de destinatários em cópia oculta
        headers (dict, optional): Headers customizados adicionais

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> send_email(
        ...     subject="Bem-vindo!",
        ...     text_content="Bem-vindo ao nosso sistema.",
        ...     recipient_list=["user@example.com"],
        ...     html_content="<h1>Bem-vindo ao nosso sistema!</h1>",
        ...     reply_to=["support@example.com"]
        ... )
        True
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Prepara o conteúdo HTML com CSS inline se necessário
        processed_html = None
        if html_content:
            if inline_css:
                try:
                    processed_html = Pynliner().from_string(html_content).run()
                except Exception as e:
                    print(f"Erro ao aplicar CSS inline: {e}")
                    processed_html = html_content
            else:
                processed_html = html_content

        # Cria email multipart (melhor compatibilidade)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Versão texto plano (fallback)
            from_email=from_email,
            to=recipient_list,
            bcc=bcc,
            reply_to=reply_to,
        )

        # Anexa versão HTML como alternativa
        if processed_html:
            msg.attach_alternative(processed_html, "text/html")

        # Adiciona headers importantes
        email_headers = {
            # Message-ID único para rastreamento e threading
            "Message-ID": f"<{uuid.uuid7()}@{from_email.split('@')[-1]}>",
            # Identificador do sistema
            "X-Mailer": "ArmoredDjango/1.0",
            # Prioridade normal
            "X-Priority": "3",
            # ID de referência único para rastreamento
            "X-Entity-Ref-ID": str(uuid.uuid7()),
        }

        # Adiciona headers customizados se fornecidos
        if headers:
            email_headers.update(headers)

        # Aplica os headers ao email
        for key, value in email_headers.items():
            msg.extra_headers[key] = value

        msg.send()
        return True

    except Exception as e:
        # Log the error in production
        print(f"Erro ao enviar email: {e}")
        return False


def load_email_template(template_path: str = None) -> str:
    """
    Carrega o template HTML base para emails.
    
    Args:
        template_path (str, optional): Caminho customizado do template
    
    Returns:
        str: Conteúdo do template HTML
    """
    if template_path is None:
        template_path = Path(__file__).parent / "email_template.html"
    else:
        template_path = Path(template_path)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao carregar template: {e}")
        # Retorna template básico como fallback
        return """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                {body_content}
            </body>
        </html>
        """


def build_email_html(
    title: str,
    header_content: str,
    body_content: str,
    footer_content: str = None,
) -> str:
    """
    Constrói o HTML do email usando o template base.
    
    Args:
        title (str): Título do email
        header_content (str): Conteúdo do cabeçalho
        body_content (str): Conteúdo principal
        footer_content (str, optional): Conteúdo do rodapé
    
    Returns:
        str: HTML completo do email
    """
    template = load_email_template()
    
    if footer_content is None:
        footer_content = "© ArmoredDjango — Todos os direitos reservados"
    
    return template.format(
        title=title,
        header_content=header_content,
        body_content=body_content,
        footer_content=footer_content,
    )


def send_welcome_email(user, custom_message: str = None) -> bool:
    """
    Envia um email de boas-vindas ao usuário com template profissional.

    Args:
        user: Objeto do usuário (Profile)
        custom_message (str, optional): Mensagem customizada adicional

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> from django.contrib.auth import get_user_model
        >>> User = get_user_model()
        >>> user = User.objects.get(username="john.doe")
        >>> send_welcome_email(user)
        True
    """
    subject = "Bem-vindo(a) ao ArmoredDjango!"
    user_name = user.get_full_name() or user.username

    text_content = f"""
    Olá {user_name},

    Seja bem-vindo(a) ao nosso sistema!

    Seu cadastro foi realizado com sucesso. A partir de agora, você pode
    utilizar o sistema para acessar todos os recursos disponíveis.

    {custom_message or ''}

    Caso tenha qualquer dúvida ou dificuldade, nossa equipe está à disposição
    para ajudar.

    Atenciosamente,
    Equipe ArmoredDjango
    """.strip()

    # Conteúdo do cabeçalho
    header_content = """
        <div style="text-align: center;">
            <h1 class="brand">ArmoredDjango</h1>
        </div>
    """

    # Conteúdo principal
    body_parts = [
        f'<p class="greeting">Olá <strong>{user_name}</strong>,</p>',
        '<p class="message">Seja bem-vindo(a) ao nosso sistema!</p>',
        '<p class="message">Seu cadastro foi realizado com sucesso.</p>',
    ]

    if custom_message:
        body_parts.append(f'<p class="message">{custom_message}</p>')

    body_parts.append("""
        <div class="signature">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """)

    body_content = "\n".join(body_parts)

    # Monta HTML completo
    html_content = build_email_html(
        title="Bem-vindo ao ArmoredDjango",
        header_content=header_content,
        body_content=body_content,
    )

    return send_email(
        subject=subject,
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


def send_password_reset_email(user, reset_url: str) -> bool:
    """
    Envia um email de redefinição de senha ao usuário com template profissional.

    Args:
        user: Objeto do usuário (Profile)
        reset_url (str): URL para redefinição de senha

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> send_password_reset_email(user, "https://example.com/reset/token123")
        True
    """
    subject = "Redefinição de Senha - ArmoredDjango"
    user_name = user.get_full_name() or user.username

    text_content = f"""
    Olá {user_name},

    Recebemos uma solicitação para redefinir sua senha.

    Para redefinir sua senha, acesse o link abaixo:
    {reset_url}

    Se você não solicitou esta redefinição, ignore este email.
    Sua senha permanecerá a mesma e nenhuma alteração será feita.

    Atenciosamente,
    Equipe ArmoredDjango
    """

    # Conteúdo do cabeçalho
    header_content = """
        <div style="text-align: center;">
            <h1 class="brand">ArmoredDjango</h1>
            <p style="color: #666; margin-top: 8px;">Redefinição de Senha</p>
        </div>
    """

    # Conteúdo principal
    body_content = f"""
        <p class="greeting">Olá <strong>{user_name}</strong>,</p>
        
        <p class="message">Recebemos uma solicitação para redefinir sua senha.</p>
        
        <p class="message">Para criar uma nova senha, clique no botão abaixo:</p>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="{reset_url}" class="button">
                Redefinir Senha
            </a>
        </div>
        
        <p style="font-size: 14px; color: #666;">
            Ou copie e cole o link abaixo no seu navegador:
        </p>
        <p style="font-size: 13px; color: #00529C; word-break: break-all;">
            {reset_url}
        </p>
        
        <div class="alert-box" style="margin-top: 24px;">
            <p class="alert-title">⚠️ Aviso de Segurança</p>
            <p class="alert-text">
                Se você não solicitou esta redefinição, ignore este email.
                Sua senha permanecerá a mesma e nenhuma alteração será feita.
            </p>
        </div>
        
        <div class="signature">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """

    # Monta HTML completo
    html_content = build_email_html(
        title="Redefinição de Senha",
        header_content=header_content,
        body_content=body_content,
    )

    return send_email(
        subject=subject,
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


def send_notification_email(
    user,
    notification_title: str,
    notification_message: str,
    action_url: str = None,
    action_label: str = "Ver Detalhes",
) -> bool:
    """
    Envia um email de notificação genérico ao usuário.

    Args:
        user: Objeto do usuário (Profile)
        notification_title (str): Título da notificação
        notification_message (str): Mensagem da notificação
        action_url (str, optional): URL para ação relacionada
        action_label (str, optional): Label do botão de ação

    Returns:
        bool: True se o email foi enviado com sucesso, False caso contrário

    Example:
        >>> send_notification_email(
        ...     user,
        ...     "Nova mensagem",
        ...     "Você recebeu uma nova mensagem no sistema.",
        ...     "https://example.com/messages/123",
        ...     "Ver Mensagem"
        ... )
        True
    """
    subject = f"{notification_title} - ArmoredDjango"
    user_name = user.get_full_name() or user.username

    text_content = f"""
    Olá {user_name},

    {notification_title}

    {notification_message}

    {f'Para mais detalhes, acesse: {action_url}' if action_url else ''}

    Atenciosamente,
    Equipe ArmoredDjango
    """

    # Conteúdo do cabeçalho
    header_content = """
        <div style="text-align: center;">
            <h1 class="brand">ArmoredDjango</h1>
            <p style="color: #666; margin-top: 8px;">Notificação</p>
        </div>
    """

    # Conteúdo principal
    body_parts = [
        f'<p class="greeting">Olá <strong>{user_name}</strong>,</p>',
        f'<h2 style="color: #00529C; margin: 24px 0 16px;">{notification_title}</h2>',
        f'<p class="message">{notification_message}</p>',
    ]

    if action_url:
        body_parts.append(f"""
            <div style="text-align: center; margin: 32px 0;">
                <a href="{action_url}" class="button">
                    {action_label}
                </a>
            </div>
        """)

    body_parts.append("""
        <div class="signature">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """)

    body_content = "\n".join(body_parts)

    # Monta HTML completo
    html_content = build_email_html(
        title=notification_title,
        header_content=header_content,
        body_content=body_content,
    )

    return send_email(
        subject=subject,
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )
