"""
Script de teste para envio de emails.

Execute no shell do Django:
    python manage.py shell < test_send_email.py

Ou copie e cole no shell:
    python manage.py shell
    >>> exec(open('utils/test_send_email.py').read())
"""

from django.contrib.auth import get_user_model
from utils.email_examples import (
    exemplo_email_cadastro_simples,
    exemplo_email_recuperacao_senha_simples,
    exemplo_notificacao_com_acao,
    exemplo_notificacao_pagamento_aprovado,
)

# Configurações
EMAIL_TESTE = "seu-email@example.com"  # ALTERE AQUI!

User = get_user_model()

print("\n" + "="*60)
print("🧪 TESTE DE ENVIO DE EMAILS")
print("="*60 + "\n")

# Verifica se há usuários no sistema
if not User.objects.exists():
    print("❌ Nenhum usuário encontrado!")
    print("💡 Crie um usuário primeiro:")
    print("   python manage.py createsuperuser\n")
    exit()

# Tenta pegar usuário admin ou o primeiro disponível
try:
    user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    print(f"✅ Usuário encontrado: {user.username} ({user.email})")
    print(f"📧 Email original: {user.email}")
    
    # Pergunta se quer trocar o email temporariamente
    print(f"\n⚠️  O email será enviado para: {EMAIL_TESTE}")
    print("💡 Altere a variável EMAIL_TESTE no início deste arquivo\n")
    
    # Salva email original
    email_original = user.email
    
    # Troca temporariamente para email de teste
    user.email = EMAIL_TESTE
    
    print("\n" + "-"*60)
    print("📨 Enviando emails de teste...")
    print("-"*60 + "\n")
    
    # 1. Email de Boas-Vindas
    print("1️⃣  Enviando email de boas-vindas...")
    try:
        resultado = exemplo_email_cadastro_simples(user)
        if resultado:
            print("   ✅ Email de boas-vindas enviado com sucesso!\n")
        else:
            print("   ❌ Falha ao enviar email de boas-vindas\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # 2. Email de Recuperação de Senha (mock)
    print("2️⃣  Enviando email de recuperação de senha...")
    try:
        # Cria request mock para teste
        class MockRequest:
            def is_secure(self):
                return False
        
        class MockSite:
            domain = "localhost:8003"
        
        class MockRequest:
            def is_secure(self):
                return False
        
        from django.contrib.sites.shortcuts import get_current_site
        from unittest.mock import Mock
        
        mock_request = Mock()
        mock_request.is_secure.return_value = False
        mock_request.META = {'HTTP_HOST': 'localhost:8003'}
        
        # Gera URL de teste
        reset_url = f"http://localhost:8003/reset/test-token-123456/"
        
        from utils.emails import send_password_reset_email
        resultado = send_password_reset_email(user, reset_url)
        
        if resultado:
            print("   ✅ Email de recuperação enviado com sucesso!\n")
        else:
            print("   ❌ Falha ao enviar email de recuperação\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # 3. Email de Notificação
    print("3️⃣  Enviando email de notificação...")
    try:
        resultado = exemplo_notificacao_com_acao(user)
        if resultado:
            print("   ✅ Email de notificação enviado com sucesso!\n")
        else:
            print("   ❌ Falha ao enviar email de notificação\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # 4. Email de Pagamento
    print("4️⃣  Enviando email de pagamento aprovado...")
    try:
        resultado = exemplo_notificacao_pagamento_aprovado(user, valor=150.00, pedido_id=123)
        if resultado:
            print("   ✅ Email de pagamento enviado com sucesso!\n")
        else:
            print("   ❌ Falha ao enviar email de pagamento\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # Restaura email original
    user.email = email_original
    user.save()
    
    print("-"*60)
    print("✅ Teste concluído!")
    print("-"*60)
    print(f"\n📬 Verifique sua caixa de entrada: {EMAIL_TESTE}")
    print("💡 Se não recebeu, verifique:")
    print("   - Configurações de SMTP no .env")
    print("   - Pasta de spam")
    print("   - Logs do console se estiver usando console backend\n")
    
except Exception as e:
    print(f"\n❌ Erro geral: {e}\n")
    import traceback
    traceback.print_exc()
