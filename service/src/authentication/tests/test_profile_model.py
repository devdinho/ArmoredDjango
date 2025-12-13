"""
Testes para o model Profile
"""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from utils.constants import ProfileType


@pytest.mark.django_db
class TestProfileModel:
    """Testes para o model Profile."""

    def test_create_profile_basic(self):
        """Testa criação básica de perfil."""
        User = get_user_model()
        user = User.objects.create_user(
            username="joao.silva",
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            password="Senha123!",
        )

        assert user.id is not None
        assert user.username == "joao.silva"
        assert user.first_name == "João"
        assert user.last_name == "Silva"
        assert user.email == "joao@example.com"
        assert user.check_password("Senha123!")

    def test_create_profile_with_profile_type(self):
        """Testa criação de perfil com tipo específico."""
        User = get_user_model()
        user = User.objects.create_user(
            username="maria.santos",
            first_name="Maria",
            last_name="Santos",
            email="maria@example.com",
            password="Senha123!",
            profileType=ProfileType.ADMIN,
        )

        assert user.profileType == ProfileType.ADMIN

    def test_profile_default_profile_type(self):
        """Testa tipo de perfil padrão."""
        User = get_user_model()
        user = User.objects.create_user(
            username="carlos.oliveira",
            first_name="Carlos",
            last_name="Oliveira",
            email="carlos@example.com",
            password="Senha123!",
        )

        assert user.profileType == ProfileType.EARUSER

    def test_profile_unique_username(self):
        """Testa que username deve ser único."""
        User = get_user_model()

        User.objects.create_user(
            username="ana.costa",
            first_name="Ana",
            last_name="Costa",
            email="ana1@example.com",
            password="Senha123!",
        )

        # Tentar criar outro usuário com mesmo username
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username="ana.costa",
                first_name="Outro",
                last_name="Usuário",
                email="ana2@example.com",
                password="Senha123!",
            )

    def test_profile_unique_email(self):
        """Testa que email deve ser único."""
        User = get_user_model()

        User.objects.create_user(
            username="pedro.almeida",
            first_name="Pedro",
            last_name="Almeida",
            email="pedro@example.com",
            password="Senha123!",
        )

        # Email duplicado deve gerar erro
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username="outro.pedro",
                first_name="Outro",
                last_name="Pedro",
                email="pedro@example.com",
                password="Senha123!",
            )

    def test_profile_superuser_created_active(self):
        """Testa que superusuários são criados como ativos."""
        User = get_user_model()
        user = User.objects.create_superuser(
            username="admin.sistema",
            first_name="Admin",
            last_name="Sistema",
            email="admin@example.com",
            password="Admin123!",
        )

        assert user.is_active
        assert user.is_superuser

    def test_profile_staff_created_active(self):
        """Testa que staff são criados como ativos."""
        User = get_user_model()
        user = User.objects.create_user(
            username="staff.user",
            first_name="Staff",
            last_name="User",
            email="staff@example.com",
            password="Staff123!",
            is_staff=True,
        )

        assert user.is_active
        assert user.is_staff

    def test_profile_str_representation(self):
        """Testa representação em string do perfil."""
        User = get_user_model()
        user = User.objects.create_user(
            username="roberto.lima",
            first_name="Roberto",
            last_name="Lima",
            email="roberto@example.com",
            password="Senha123!",
        )

        str_repr = str(user)

        assert "Roberto" in str_repr
        assert "Lima" in str_repr
        assert "roberto.lima" in str_repr

    def test_profile_get_full_name(self):
        """Testa método get_full_name."""
        User = get_user_model()
        user = User.objects.create_user(
            username="fernanda.rocha",
            first_name="Fernanda",
            last_name="Rocha",
            email="fernanda@example.com",
            password="Senha123!",
        )

        full_name = user.get_full_name()

        assert full_name == "Fernanda Rocha"

    def test_profile_groups_relationship(self):
        """Testa relacionamento many-to-many com grupos."""
        from authentication.models import Groups

        User = get_user_model()
        user = User.objects.create_user(
            username="ricardo.gomes",
            first_name="Ricardo",
            last_name="Gomes",
            email="ricardo@example.com",
            password="Senha123!",
        )

        # Criar grupos
        group1 = Groups.objects.create(name="Gestores")
        group2 = Groups.objects.create(name="Analistas")

        # Adicionar usuário aos grupos
        user.groups.add(group1, group2)

        assert group1 in user.groups.all()
        assert group2 in user.groups.all()
        assert user.groups.count() == 2

    def test_profile_user_permissions_relationship(self):
        """Testa relacionamento many-to-many com permissões."""
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        User = get_user_model()
        user = User.objects.create_user(
            username="patricia.vieira",
            first_name="Patrícia",
            last_name="Vieira",
            email="patricia@example.com",
            password="Senha123!",
        )

        # Obter uma permissão
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.filter(content_type=content_type).first()

        if permission:
            user.user_permissions.add(permission)
            assert permission in user.user_permissions.all()

    def test_profile_history_tracking(self):
        """Testa que histórico é rastreado."""
        User = get_user_model()
        user = User.objects.create_user(
            username="marcos.pereira",
            first_name="Marcos",
            last_name="Pereira",
            email="marcos@example.com",
            password="Senha123!",
        )

        # Verificar que histórico foi criado
        assert user.history.count() == 1

        # Atualizar usuário
        user.first_name = "Marcos Antonio"
        user.save()

        # Verificar que novo registro de histórico foi criado
        assert user.history.count() == 2

    def test_profile_different_profile_types(self):
        """Testa diferentes tipos de perfil."""
        User = get_user_model()

        # EARUSER
        user1 = User.objects.create_user(
            username="user.earuser",
            first_name="User1",
            last_name="Test",
            email="user1@example.com",
            password="Senha123!",
            profileType=ProfileType.EARUSER,
        )

        # ADMIN
        user2 = User.objects.create_user(
            username="user.admin",
            first_name="Admin",
            last_name="User",
            email="admin2@example.com",
            password="Senha123!",
            profileType=ProfileType.ADMIN,
        )

        assert user2.profileType == ProfileType.ADMIN
        assert user1.profileType != user2.profileType

    def test_profile_password_hashing(self):
        """Testa que senha é hasheada."""
        User = get_user_model()
        password = "SenhaOriginal123!"

        user = User.objects.create_user(
            username="teste.hash",
            first_name="Teste",
            last_name="Hash",
            email="hash@example.com",
            password=password,
        )

        # Senha não deve estar armazenada em texto plano
        assert user.password != password

        # Mas deve ser verificável
        assert user.check_password(password)
        assert not user.check_password("SenhaErrada")

    def test_profile_update_fields(self):
        """Testa atualização de campos do perfil."""
        User = get_user_model()
        user = User.objects.create_user(
            username="original.name",
            first_name="Original",
            last_name="Name",
            email="original@example.com",
            password="Senha123!",
        )

        # Atualizar campos
        user.first_name = "Updated"
        user.email = "updated@example.com"
        user.save()

        # Recarregar do banco
        user.refresh_from_db()

        assert user.first_name == "Updated"
        assert user.email == "updated@example.com"
        assert user.last_name == "Name"  # Não mudou

    def test_profile_is_active_can_be_changed(self):
        """Testa que is_active pode ser alterado."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.active",
            first_name="Test",
            last_name="Active",
            email="active@example.com",
            password="Senha123!",
        )

        # Deve ser criado ativo (comportamento padrão do Django)
        assert user.is_active

        # Desativar
        user.is_active = False
        user.save()

        user.refresh_from_db()
        assert not user.is_active

        # Ativar novamente
        user.is_active = True
        user.save()

        user.refresh_from_db()
        assert user.is_active
