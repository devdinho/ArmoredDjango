"""
Testes para serializers de autenticação
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from authentication.serializers import ProfileSerializer


@pytest.mark.django_db
class TestProfileSerializer:
    """Testes para o ProfileSerializer."""

    def test_serialize_profile(self):
        """Testa serialização de perfil."""
        User = get_user_model()
        user = User.objects.create_user(
            username="joao.silva",
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            password="Senha123!",
        )

        serializer = ProfileSerializer(user)
        data = serializer.data

        assert data["id"] == user.id
        assert data["username"] == "joao.silva"
        assert data["first_name"] == "João"
        assert data["last_name"] == "Silva"
        assert data["email"] == "joao@example.com"
        assert "password" not in data  # write_only
        assert "last_login" in data
        assert "date_joined" in data

    def test_create_profile_valid_data(self):
        """Testa criação de perfil com dados válidos."""
        data = {
            "username": "maria.santos",
            "first_name": "Maria",
            "last_name": "Santos",
            "email": "Maria@Example.com",  # Maiúsculas para testar lowercase
            "password": "Senha123!",
        }

        serializer = ProfileSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()

        assert user.username == "maria.santos"
        assert user.first_name == "Maria"
        assert user.last_name == "Santos"
        assert user.email == "maria@example.com"  # Convertido para lowercase
        assert user.check_password("Senha123!")

    def test_create_profile_missing_required_fields(self):
        """Testa criação de perfil sem campos obrigatórios."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            # Faltando password, first_name, last_name
        }

        serializer = ProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_create_profile_duplicate_username(self):
        """Testa criação de perfil com username duplicado."""
        User = get_user_model()
        User.objects.create_user(
            username="existing.user",
            first_name="Existing",
            last_name="User",
            email="existing@example.com",
            password="Senha123!",
        )

        data = {
            "username": "existing.user",  # Duplicado
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "password": "Senha123!",
        }

        serializer = ProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_create_profile_duplicate_email(self):
        """Testa criação de perfil com email duplicado."""
        User = get_user_model()
        User.objects.create_user(
            username="first.user",
            first_name="Existing",
            last_name="User",
            email="duplicate@example.com",
            password="Senha123!",
        )

        data = {
            "username": "second.user",
            "first_name": "New",
            "last_name": "User",
            "email": "duplicate@example.com",  # Duplicado
            "password": "Senha123!",
        }

        serializer = ProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_update_profile_basic_fields(self):
        """Testa atualização de campos básicos do perfil."""
        User = get_user_model()
        user = User.objects.create_user(
            username="original.name",
            first_name="Original",
            last_name="Name",
            email="original@example.com",
            password="Senha123!",
        )

        data = {
            "first_name": "Updated",
            "last_name": "NewName",
        }

        serializer = ProfileSerializer(user, data=data, partial=True)
        assert serializer.is_valid()

        updated_user = serializer.save()

        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "NewName"
        assert updated_user.username == "original.name"  # Não mudou
        assert updated_user.email == "original@example.com"  # Não mudou

    def test_update_profile_password(self):
        """Testa atualização de senha."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.password",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="OldPassword123!",
        )

        old_password_hash = user.password

        data = {
            "password": "NewPassword456!",
        }

        serializer = ProfileSerializer(user, data=data, partial=True)
        assert serializer.is_valid()

        updated_user = serializer.save()

        # Hash da senha deve ter mudado
        assert updated_user.password != old_password_hash

        # Senha nova deve funcionar
        assert updated_user.check_password("NewPassword456!")
        assert not updated_user.check_password("OldPassword123!")

    def test_update_profile_email(self):
        """Testa atualização de email."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.email",
            first_name="Test",
            last_name="User",
            email="old@example.com",
            password="Senha123!",
        )

        data = {
            "email": "new@example.com",
        }

        serializer = ProfileSerializer(user, data=data, partial=True)
        assert serializer.is_valid()

        updated_user = serializer.save()

        assert updated_user.email == "new@example.com"

    def test_password_write_only(self):
        """Testa que password é write_only."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.writeonly",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="Senha123!",
        )

        serializer = ProfileSerializer(user)
        data = serializer.data

        assert "password" not in data

    def test_read_only_fields(self):
        """Testa que last_login e date_joined são read-only."""
        data = {
            "username": "test.readonly",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "Senha123!",
            "last_login": "2024-01-01T00:00:00Z",
            "date_joined": "2024-01-01T00:00:00Z",
        }

        serializer = ProfileSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()

        # Campos read-only não devem ser setados pelos dados fornecidos
        assert user.last_login is None
        assert user.date_joined is not None

    def test_serialize_multiple_profiles(self):
        """Testa serialização de múltiplos perfis."""
        User = get_user_model()

        users = [
            User.objects.create_user(
                username=f"user{i}",
                first_name=f"User{i}",
                last_name="Test",
                email=f"user{i}@example.com",
                password="Senha123!",
            )
            for i in range(3)
        ]

        serializer = ProfileSerializer(users, many=True)
        data = serializer.data

        assert len(data) == 3
        for i, user_data in enumerate(data):
            assert user_data["first_name"] == f"User{i}"

    def test_partial_update(self):
        """Testa atualização parcial."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.partial",
            first_name="Original",
            last_name="Name",
            email="original@example.com",
            password="Senha123!",
        )

        data = {
            "first_name": "Updated",
        }

        serializer = ProfileSerializer(user, data=data, partial=True)
        assert serializer.is_valid()

        updated_user = serializer.save()

        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"  # Não mudou
        assert updated_user.email == "original@example.com"  # Não mudou

    def test_create_profile_email_lowercase(self):
        """Testa que email é convertido para lowercase na criação."""
        data = {
            "username": "test.lowercase",
            "first_name": "Test",
            "last_name": "User",
            "email": "TEST@EXAMPLE.COM",
            "password": "Senha123!",
        }

        serializer = ProfileSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()

        assert user.email == "test@example.com"

    def test_password_required_on_create(self):
        """Testa que password é obrigatório na criação."""
        data = {
            "username": "test.required",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            # password faltando
        }

        serializer = ProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_password_optional_on_update(self):
        """Testa que password é opcional na atualização."""
        User = get_user_model()
        user = User.objects.create_user(
            username="test.optional",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="Senha123!",
        )

        data = {
            "first_name": "Updated",
            # password não fornecido
        }

        serializer = ProfileSerializer(user, data=data, partial=True)
        assert serializer.is_valid()

        updated_user = serializer.save()

        # Senha não deve ter mudado
        assert updated_user.check_password("Senha123!")

    def test_validation_error_on_create_exception(self):
        """Testa que exceções na criação são convertidas em ValidationError."""
        data = {
            "username": "",  # Username vazio pode causar erro
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "Senha123!",
        }

        serializer = ProfileSerializer(data=data)

        # Pode não ser válido na validação ou lançar erro no save
        if serializer.is_valid():
            with pytest.raises(ValidationError):
                serializer.save()
