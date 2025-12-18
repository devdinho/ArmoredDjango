"""
Comando Django para testar envio de emails.

Uso:
    python manage.py test_email seu-email@example.com
    python manage.py test_email seu-email@example.com --tipo=cadastro
    python manage.py test_email seu-email@example.com --tipo=recuperacao
    python manage.py test_email seu-email@example.com --tipo=notificacao
    python manage.py test_email seu-email@example.com --tipo=pagamento
    python manage.py test_email seu-email@example.com --tipo=todos
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Testa o envio de emails para um endereço específico'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email de destino para teste'
        )
        parser.add_argument(
            '--tipo',
            type=str,
            default='todos',
            choices=['cadastro', 'recuperacao', 'notificacao', 'pagamento', 'todos'],
            help='Tipo de email para testar (padrão: todos)'
        )
        parser.add_argument(
            '--username',
            type=str,
            default=None,
            help='Username do usuário para usar no teste (padrão: admin ou primeiro usuário)'
        )

    def handle(self, *args, **options):
        email_destino = options['email']
        tipo_email = options['tipo']
        username = options['username']
        
        User = get_user_model()
        
        # Valida email
        if '@' not in email_destino:
            raise CommandError(f'Email inválido: {email_destino}')
        
        # Busca usuário
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f'Usuário não encontrado: {username}')
        else:
            user = User.objects.filter(is_superuser=True).first() or User.objects.first()
            
            if not user:
                raise CommandError(
                    'Nenhum usuário encontrado! Crie um usuário primeiro:\n'
                    '  python manage.py createsuperuser'
                )
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS('🧪 TESTE DE ENVIO DE EMAILS'))
        self.stdout.write("="*60 + "\n")
        
        self.stdout.write(f"✅ Usuário: {user.username} ({user.email})")
        self.stdout.write(f"📧 Destino: {email_destino}\n")
        
        # Salva email original
        email_original = user.email
        user.email = email_destino
        
        resultados = []
        
        try:
            # 1. Email de Cadastro
            if tipo_email in ['cadastro', 'todos']:
                self.stdout.write("-"*60)
                self.stdout.write("1️⃣  Email de Cadastro/Boas-Vindas")
                self.stdout.write("-"*60)
                
                from utils.email_examples import exemplo_email_cadastro_simples
                try:
                    resultado = exemplo_email_cadastro_simples(user)
                    if resultado:
                        self.stdout.write(self.style.SUCCESS("   ✅ Enviado com sucesso!\n"))
                        resultados.append(('Cadastro', True))
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ Falha no envio\n"))
                        resultados.append(('Cadastro', False))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ Erro: {e}\n"))
                    resultados.append(('Cadastro', False))
            
            # 2. Email de Recuperação de Senha
            if tipo_email in ['recuperacao', 'todos']:
                self.stdout.write("-"*60)
                self.stdout.write("2️⃣  Email de Recuperação de Senha")
                self.stdout.write("-"*60)
                
                from utils.emails import send_password_reset_email
                try:
                    reset_url = "http://localhost:8003/reset/test-token-abc123/"
                    resultado = send_password_reset_email(user, reset_url)
                    if resultado:
                        self.stdout.write(self.style.SUCCESS("   ✅ Enviado com sucesso!\n"))
                        resultados.append(('Recuperação', True))
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ Falha no envio\n"))
                        resultados.append(('Recuperação', False))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ Erro: {e}\n"))
                    resultados.append(('Recuperação', False))
            
            # 3. Email de Notificação
            if tipo_email in ['notificacao', 'todos']:
                self.stdout.write("-"*60)
                self.stdout.write("3️⃣  Email de Notificação")
                self.stdout.write("-"*60)
                
                from utils.email_examples import exemplo_notificacao_com_acao
                try:
                    resultado = exemplo_notificacao_com_acao(user)
                    if resultado:
                        self.stdout.write(self.style.SUCCESS("   ✅ Enviado com sucesso!\n"))
                        resultados.append(('Notificação', True))
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ Falha no envio\n"))
                        resultados.append(('Notificação', False))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ Erro: {e}\n"))
                    resultados.append(('Notificação', False))
            
            # 4. Email de Pagamento
            if tipo_email in ['pagamento', 'todos']:
                self.stdout.write("-"*60)
                self.stdout.write("4️⃣  Email de Pagamento Aprovado")
                self.stdout.write("-"*60)
                
                from utils.email_examples import exemplo_notificacao_pagamento_aprovado
                try:
                    resultado = exemplo_notificacao_pagamento_aprovado(
                        user, 
                        valor=150.00, 
                        pedido_id=123
                    )
                    if resultado:
                        self.stdout.write(self.style.SUCCESS("   ✅ Enviado com sucesso!\n"))
                        resultados.append(('Pagamento', True))
                    else:
                        self.stdout.write(self.style.ERROR("   ❌ Falha no envio\n"))
                        resultados.append(('Pagamento', False))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ Erro: {e}\n"))
                    resultados.append(('Pagamento', False))
            
        finally:
            # Restaura email original
            user.email = email_original
            user.save()
        
        # Resumo
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS('📊 RESUMO'))
        self.stdout.write("="*60 + "\n")
        
        total = len(resultados)
        sucesso = sum(1 for _, ok in resultados if ok)
        falhas = total - sucesso
        
        for tipo, ok in resultados:
            status = self.style.SUCCESS('✅') if ok else self.style.ERROR('❌')
            self.stdout.write(f"  {status} {tipo}")
        
        self.stdout.write(f"\n  Total: {total} | Sucesso: {sucesso} | Falhas: {falhas}\n")
        
        self.stdout.write("-"*60)
        self.stdout.write(f"📬 Verifique sua caixa de entrada: {email_destino}")
        self.stdout.write("\n💡 Se não recebeu, verifique:")
        self.stdout.write("   - Configurações de SMTP no .env")
        self.stdout.write("   - Pasta de spam")
        self.stdout.write("   - Logs do console (se estiver usando console backend)")
        self.stdout.write("="*60 + "\n")
