"""
Exemplos práticos de uso do sistema de emails do ArmoredDjango.

Este arquivo contém scripts de exemplo para os principais cenários de envio de email.
Copie e adapte conforme necessário para seu projeto.
"""

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from utils.emails import (
    send_welcome_email,
    send_password_reset_email,
    send_notification_email,
    send_email,
    build_email_html,
)


# ==============================================================================
# 1. EMAIL DE CADASTRO / BOAS-VINDAS
# ==============================================================================

def exemplo_email_cadastro_simples(user):
    """
    Exemplo 1: Email de boas-vindas simples após cadastro.
    
    Quando usar: Logo após criar um novo usuário no sistema.
    """
    # Forma mais simples - usa o template padrão
    resultado = send_welcome_email(user)
    
    if resultado:
        print(f"✅ Email de boas-vindas enviado para {user.email}")
    else:
        print(f"❌ Falha ao enviar email para {user.email}")
    
    return resultado


def exemplo_email_cadastro_com_mensagem_customizada(user):
    """
    Exemplo 2: Email de boas-vindas com mensagem personalizada.
    
    Quando usar: Quando você quer adicionar informações extras, como
    promoções, instruções especiais, etc.
    """
    mensagem_extra = """
    🎉 Como presente de boas-vindas, você ganhou 30 dias de teste premium!
    
    Aproveite todos os recursos avançados do nosso sistema sem custo adicional.
    """
    
    resultado = send_welcome_email(user, custom_message=mensagem_extra)
    
    return resultado


def exemplo_email_cadastro_completo_customizado(user, request):
    """
    Exemplo 3: Email de cadastro totalmente customizado.
    
    Quando usar: Quando você precisa de um design ou conteúdo muito específico.
    """
    domain = get_current_site(request).domain
    user_name = user.get_full_name() or user.username
    
    # Conteúdo do cabeçalho
    header_content = """
        <div style="text-align: center;">
            <h1 style="color: #00529C;">Bem-vindo ao ArmoredDjango!</h1>
            <p style="color: #666;">Sua jornada começa aqui</p>
        </div>
    """
    
    # Conteúdo principal
    body_content = f"""
        <p style="font-size: 16px;">
            Olá <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 15px;">
            É um prazer ter você conosco! Seu cadastro foi realizado com sucesso.
        </p>
        
        <div style="background-color: #f0f9ff; border-left: 4px solid #00529C; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-weight: bold; color: #00529C;">
                🎁 Bônus de Boas-Vindas
            </p>
            <p style="margin: 8px 0 0 0; font-size: 14px;">
                Ganhe 30 dias de acesso premium gratuitamente!
            </p>
        </div>
        
        <h3 style="color: #00529C; margin-top: 32px;">Próximos Passos:</h3>
        <ol style="font-size: 14px; line-height: 1.8;">
            <li>Complete seu perfil</li>
            <li>Explore nossos recursos</li>
            <li>Configure suas preferências</li>
        </ol>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://{domain}/dashboard" 
               style="display: inline-block; padding: 12px 32px;
                      background-color: #00529C; color: #ffffff;
                      text-decoration: none; border-radius: 4px; font-size: 16px;">
                Acessar Meu Painel
            </a>
        </div>
        
        <p style="font-size: 14px; color: #666; margin-top: 32px;">
            Se tiver dúvidas, nossa equipe está à disposição para ajudar.
        </p>
        
        <div style="margin-top: 32px; font-size: 14px;">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """
    
    # Monta HTML completo
    html_content = build_email_html(
        title="Bem-vindo ao ArmoredDjango",
        header_content=header_content,
        body_content=body_content,
    )
    
    # Versão texto plano (fallback)
    text_content = f"""
    Olá {user_name},
    
    É um prazer ter você conosco! Seu cadastro foi realizado com sucesso.
    
    🎁 BÔNUS DE BOAS-VINDAS
    Ganhe 30 dias de acesso premium gratuitamente!
    
    PRÓXIMOS PASSOS:
    1. Complete seu perfil
    2. Explore nossos recursos
    3. Configure suas preferências
    
    Acesse seu painel: https://{domain}/dashboard
    
    Se tiver dúvidas, nossa equipe está à disposição para ajudar.
    
    Atenciosamente,
    Equipe ArmoredDjango
    """
    
    return send_email(
        subject="🎉 Bem-vindo ao ArmoredDjango!",
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


# ==============================================================================
# 2. EMAIL DE RECUPERAÇÃO DE SENHA
# ==============================================================================

def exemplo_email_recuperacao_senha_simples(user, request):
    """
    Exemplo 1: Email de recuperação de senha simples.
    
    Quando usar: Quando usuário clica em "Esqueci minha senha".
    """
    # Gera token de reset
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Monta URL de reset
    domain = get_current_site(request).domain
    protocol = 'https' if request.is_secure() else 'http'
    reset_url = f"{protocol}://{domain}/reset/{uid}/{token}/"
    
    # Envia email
    resultado = send_password_reset_email(user, reset_url)
    
    if resultado:
        print(f"✅ Email de reset enviado para {user.email}")
    else:
        print(f"❌ Falha ao enviar email de reset")
    
    return resultado


def exemplo_email_recuperacao_senha_com_expiracao(user, request, tempo_expiracao="1 hora"):
    """
    Exemplo 2: Email de recuperação com informação de expiração do link.
    
    Quando usar: Quando você quer deixar claro o tempo de validade do link.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    protocol = 'https' if request.is_secure() else 'http'
    reset_url = f"{protocol}://{domain}/reset/{uid}/{token}/"
    
    user_name = user.get_full_name() or user.username
    
    # Cabeçalho
    header_content = """
        <div style="text-align: center;">
            <h1 style="color: #00529C;">Redefinição de Senha</h1>
            <p style="color: #666;">Solicitação de nova senha</p>
        </div>
    """
    
    # Corpo com informação de expiração
    body_content = f"""
        <p style="font-size: 16px;">
            Olá <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 15px;">
            Recebemos uma solicitação para redefinir sua senha.
        </p>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="{reset_url}" 
               style="display: inline-block; padding: 12px 32px;
                      background-color: #00529C; color: #ffffff;
                      text-decoration: none; border-radius: 4px; font-size: 16px;">
                Redefinir Minha Senha
            </a>
        </div>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-weight: bold; color: #856404;">
                ⏰ Atenção ao Prazo
            </p>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #856404;">
                Este link é válido por apenas <strong>{tempo_expiracao}</strong>.
                Após esse período, será necessário solicitar um novo link.
            </p>
        </div>
        
        <p style="font-size: 13px; color: #666;">
            Ou copie e cole o link abaixo no seu navegador:
        </p>
        <p style="font-size: 12px; color: #00529C; word-break: break-all;">
            {reset_url}
        </p>
        
        <div style="background-color: #f8d7da; border-left: 4px solid #dc3545; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-weight: bold; color: #721c24;">
                🔒 Aviso de Segurança
            </p>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #721c24;">
                Se você não solicitou esta redefinição, ignore este email.
                Sua senha permanecerá a mesma e nenhuma alteração será feita.
            </p>
        </div>
        
        <div style="margin-top: 32px; font-size: 14px;">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """
    
    html_content = build_email_html(
        title="Redefinição de Senha",
        header_content=header_content,
        body_content=body_content,
    )
    
    text_content = f"""
    Olá {user_name},
    
    Recebemos uma solicitação para redefinir sua senha.
    
    Para criar uma nova senha, acesse o link abaixo:
    {reset_url}
    
    ⏰ ATENÇÃO: Este link é válido por apenas {tempo_expiracao}.
    
    🔒 SEGURANÇA: Se você não solicitou esta redefinição, ignore este email.
    
    Atenciosamente,
    Equipe ArmoredDjango
    """
    
    return send_email(
        subject="Redefinição de Senha - ArmoredDjango",
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


# ==============================================================================
# 3. EMAIL DE NOTIFICAÇÃO GENÉRICA
# ==============================================================================

def exemplo_notificacao_simples(user):
    """
    Exemplo 1: Notificação simples sem ação.
    
    Quando usar: Para informar algo ao usuário sem necessidade de ação.
    """
    return send_notification_email(
        user=user,
        notification_title="Atualização Concluída",
        notification_message="Seu perfil foi atualizado com sucesso.",
    )


def exemplo_notificacao_com_acao(user):
    """
    Exemplo 2: Notificação com botão de ação.
    
    Quando usar: Quando você quer que o usuário faça algo específico.
    """
    return send_notification_email(
        user=user,
        notification_title="Nova Mensagem",
        notification_message="Você recebeu uma nova mensagem de João Silva.",
        action_url="https://example.com/messages/123",
        action_label="Ver Mensagem",
    )


def exemplo_notificacao_pagamento_aprovado(user, valor, pedido_id):
    """
    Exemplo 3: Notificação de pagamento aprovado.
    
    Quando usar: Após confirmação de pagamento.
    """
    mensagem = f"""
    Seu pagamento de <strong>R$ {valor:.2f}</strong> foi aprovado com sucesso!
    
    <p style="font-size: 14px; color: #666; margin-top: 16px;">
    Você já pode acessar seu pedido e acompanhar o status da entrega.
    </p>
    """
    
    return send_notification_email(
        user=user,
        notification_title="💳 Pagamento Aprovado",
        notification_message=mensagem,
        action_url=f"https://example.com/pedidos/{pedido_id}",
        action_label="Ver Pedido",
    )


def exemplo_notificacao_login_novo_dispositivo(user, dispositivo, localizacao, ip):
    """
    Exemplo 4: Alerta de segurança - login de novo dispositivo.
    
    Quando usar: Para alertar sobre atividade suspeita.
    """
    user_name = user.get_full_name() or user.username
    
    header_content = """
        <div style="text-align: center;">
            <h1 style="color: #dc3545;">⚠️ Alerta de Segurança</h1>
            <p style="color: #666;">Novo acesso detectado</p>
        </div>
    """
    
    body_content = f"""
        <p style="font-size: 16px;">
            Olá <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 15px;">
            Detectamos um novo acesso à sua conta de um dispositivo não reconhecido.
        </p>
        
        <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; 
                    padding: 16px; margin: 24px 0; border-radius: 4px;">
            <h3 style="margin: 0 0 12px 0; color: #333;">Detalhes do Acesso:</h3>
            <table style="width: 100%; font-size: 14px;">
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Dispositivo:</strong></td>
                    <td style="padding: 8px 0;">{dispositivo}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Localização:</strong></td>
                    <td style="padding: 8px 0;">{localizacao}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>IP:</strong></td>
                    <td style="padding: 8px 0;">{ip}</td>
                </tr>
            </table>
        </div>
        
        <div style="background-color: #f8d7da; border-left: 4px solid #dc3545; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-weight: bold; color: #721c24;">
                Foi você?
            </p>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #721c24;">
                Se você reconhece este acesso, pode ignorar este email.
                Caso contrário, recomendamos alterar sua senha imediatamente.
            </p>
        </div>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://example.com/security/change-password" 
               style="display: inline-block; padding: 12px 32px;
                      background-color: #dc3545; color: #ffffff;
                      text-decoration: none; border-radius: 4px; font-size: 16px;">
                Alterar Senha Agora
            </a>
        </div>
        
        <div style="margin-top: 32px; font-size: 14px;">
            <p>Atenciosamente,<br>
            <strong>Equipe de Segurança ArmoredDjango</strong></p>
        </div>
    """
    
    html_content = build_email_html(
        title="Alerta de Segurança",
        header_content=header_content,
        body_content=body_content,
    )
    
    text_content = f"""
    ⚠️ ALERTA DE SEGURANÇA
    
    Olá {user_name},
    
    Detectamos um novo acesso à sua conta de um dispositivo não reconhecido.
    
    DETALHES DO ACESSO:
    - Dispositivo: {dispositivo}
    - Localização: {localizacao}
    - IP: {ip}
    
    FOI VOCÊ?
    Se você reconhece este acesso, pode ignorar este email.
    Caso contrário, altere sua senha imediatamente:
    https://example.com/security/change-password
    
    Atenciosamente,
    Equipe de Segurança ArmoredDjango
    """
    
    return send_email(
        subject="⚠️ Alerta de Segurança - Novo Dispositivo Detectado",
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


# ==============================================================================
# 4. OUTROS TIPOS DE EMAILS ÚTEIS
# ==============================================================================

def exemplo_email_confirmacao_email(user, confirmation_url):
    """
    Email de confirmação de endereço de email.
    
    Quando usar: Após cadastro, para validar o email do usuário.
    """
    user_name = user.get_full_name() or user.username
    
    header_content = """
        <div style="text-align: center;">
            <h1 style="color: #00529C;">Confirme seu Email</h1>
            <p style="color: #666;">Último passo para ativar sua conta</p>
        </div>
    """
    
    body_content = f"""
        <p style="font-size: 16px;">
            Olá <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 15px;">
            Para ativar sua conta e acessar todos os recursos, 
            precisamos confirmar seu endereço de email.
        </p>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="{confirmation_url}" 
               style="display: inline-block; padding: 12px 32px;
                      background-color: #28a745; color: #ffffff;
                      text-decoration: none; border-radius: 4px; font-size: 16px;">
                Confirmar Meu Email
            </a>
        </div>
        
        <p style="font-size: 13px; color: #666;">
            Ou copie e cole o link abaixo no seu navegador:
        </p>
        <p style="font-size: 12px; color: #00529C; word-break: break-all;">
            {confirmation_url}
        </p>
        
        <div style="background-color: #fff8e1; border-left: 4px solid #ffc107; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-size: 14px; color: #856404;">
                Se você não se cadastrou em nosso sistema, pode ignorar este email.
            </p>
        </div>
        
        <div style="margin-top: 32px; font-size: 14px;">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """
    
    html_content = build_email_html(
        title="Confirme seu Email",
        header_content=header_content,
        body_content=body_content,
    )
    
    text_content = f"""
    Olá {user_name},
    
    Para ativar sua conta e acessar todos os recursos, 
    precisamos confirmar seu endereço de email.
    
    Confirme seu email acessando:
    {confirmation_url}
    
    Se você não se cadastrou em nosso sistema, pode ignorar este email.
    
    Atenciosamente,
    Equipe ArmoredDjango
    """
    
    return send_email(
        subject="✉️ Confirme seu Email - ArmoredDjango",
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


def exemplo_email_mudanca_senha_confirmacao(user):
    """
    Confirmação após mudança de senha bem-sucedida.
    
    Quando usar: Logo após o usuário alterar a senha com sucesso.
    """
    user_name = user.get_full_name() or user.username
    
    mensagem = f"""
    Sua senha foi alterada com sucesso em {user.last_login or 'agora'}.
    
    <div style="background-color: #d1ecf1; border-left: 4px solid #17a2b8; 
                padding: 16px; margin: 24px 0;">
        <p style="margin: 0; font-size: 14px; color: #0c5460;">
            Se você não reconhece esta alteração, entre em contato com 
            nossa equipe de suporte imediatamente.
        </p>
    </div>
    """
    
    return send_notification_email(
        user=user,
        notification_title="🔒 Senha Alterada com Sucesso",
        notification_message=mensagem,
        action_url="https://example.com/security",
        action_label="Ver Configurações de Segurança",
    )


def exemplo_email_exclusao_conta(user, dias_para_exclusao=30):
    """
    Confirmação de solicitação de exclusão de conta.
    
    Quando usar: Quando usuário solicita exclusão da conta.
    """
    user_name = user.get_full_name() or user.username
    
    header_content = """
        <div style="text-align: center;">
            <h1 style="color: #dc3545;">Exclusão de Conta</h1>
            <p style="color: #666;">Lamentamos ver você partir</p>
        </div>
    """
    
    body_content = f"""
        <p style="font-size: 16px;">
            Olá <strong>{user_name}</strong>,
        </p>
        
        <p style="font-size: 15px;">
            Recebemos sua solicitação de exclusão de conta.
        </p>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; 
                    padding: 16px; margin: 24px 0;">
            <p style="margin: 0; font-weight: bold; color: #856404;">
                ⏰ Período de Retenção
            </p>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #856404;">
                Sua conta será mantida inativa por <strong>{dias_para_exclusao} dias</strong>.
                Durante este período, você pode cancelar a exclusão a qualquer momento
                fazendo login normalmente.
            </p>
        </div>
        
        <p style="font-size: 14px;">
            <strong>O que será excluído:</strong>
        </p>
        <ul style="font-size: 14px; line-height: 1.8;">
            <li>Dados pessoais</li>
            <li>Histórico de atividades</li>
            <li>Configurações de perfil</li>
            <li>Todos os dados associados à sua conta</li>
        </ul>
        
        <div style="text-align: center; margin: 32px 0;">
            <a href="https://example.com/account/cancel-deletion" 
               style="display: inline-block; padding: 12px 32px;
                      background-color: #28a745; color: #ffffff;
                      text-decoration: none; border-radius: 4px; font-size: 16px;">
                Cancelar Exclusão
            </a>
        </div>
        
        <p style="font-size: 14px; color: #666; margin-top: 32px;">
            Gostaríamos de saber o motivo da sua saída. 
            Sua opinião é muito importante para melhorarmos nossos serviços.
        </p>
        
        <div style="margin-top: 32px; font-size: 14px;">
            <p>Atenciosamente,<br>
            <strong>Equipe ArmoredDjango</strong></p>
        </div>
    """
    
    html_content = build_email_html(
        title="Exclusão de Conta",
        header_content=header_content,
        body_content=body_content,
    )
    
    text_content = f"""
    Olá {user_name},
    
    Recebemos sua solicitação de exclusão de conta.
    
    ⏰ PERÍODO DE RETENÇÃO:
    Sua conta será mantida inativa por {dias_para_exclusao} dias.
    Durante este período, você pode cancelar a exclusão fazendo login.
    
    O QUE SERÁ EXCLUÍDO:
    - Dados pessoais
    - Histórico de atividades
    - Configurações de perfil
    - Todos os dados associados à sua conta
    
    Para cancelar a exclusão:
    https://example.com/account/cancel-deletion
    
    Atenciosamente,
    Equipe ArmoredDjango
    """
    
    return send_email(
        subject="⚠️ Confirmação de Exclusão de Conta - ArmoredDjango",
        text_content=text_content,
        recipient_list=[user.email],
        html_content=html_content,
    )


# ==============================================================================
# COMO USAR ESTES EXEMPLOS
# ==============================================================================

"""
Para usar qualquer um destes exemplos em suas views ou signals:

# views.py
from utils.email_examples import exemplo_email_cadastro_simples

def register_view(request):
    # ... lógica de criação do usuário ...
    user = User.objects.create_user(...)
    
    # Envia email de boas-vindas
    exemplo_email_cadastro_simples(user)
    
    return redirect('success')


# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.email_examples import exemplo_email_cadastro_simples

@receiver(post_save, sender=User)
def send_welcome_email_on_signup(sender, instance, created, **kwargs):
    if created:
        exemplo_email_cadastro_simples(instance)


# views de autenticação
from utils.email_examples import exemplo_email_recuperacao_senha_simples

def forgot_password_view(request):
    email = request.POST.get('email')
    user = User.objects.get(email=email)
    exemplo_email_recuperacao_senha_simples(user, request)
    return redirect('password_reset_sent')
"""
