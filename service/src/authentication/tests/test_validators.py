"""
Testes para validators de autenticação
"""

import pytest
from django.core.exceptions import ValidationError

from authentication.validators import ComplexPasswordValidator


class TestComplexPasswordValidator:
    """Testes para o ComplexPasswordValidator."""

    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.validator = ComplexPasswordValidator()

    def test_validate_password_with_all_requirements(self):
        """Testa senha que atende todos os requisitos."""
        valid_passwords = [
            "SenhaForte123!",
            "MyP@ssw0rd",
            "C0mpl3x!ty",
            "Abc123!@#",
            "Test@2024Pass",
        ]

        for password in valid_passwords:
            # Não deve lançar exceção
            self.validator.validate(password)

    def test_validate_password_without_uppercase(self):
        """Testa senha sem letra maiúscula."""
        password_no_upper = "senhafraca123!"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password_no_upper)

        assert exc_info.value.code == "password_no_upper"
        assert "maiúscula" in str(exc_info.value)

    def test_validate_password_without_lowercase(self):
        """Testa senha sem letra minúscula."""
        password_no_lower = "SENHAFRACA123!"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password_no_lower)

        assert exc_info.value.code == "password_no_lower"
        assert "minúscula" in str(exc_info.value)

    def test_validate_password_without_number(self):
        """Testa senha sem número."""
        password_no_number = "SenhaFraca!@#"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password_no_number)

        assert exc_info.value.code == "password_no_number"
        assert "número" in str(exc_info.value)

    def test_validate_password_without_special_character(self):
        """Testa senha sem caractere especial."""
        password_no_special = "SenhaFraca123"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password_no_special)

        assert exc_info.value.code == "password_no_symbol"
        assert "caractere especial" in str(exc_info.value)

    def test_validate_password_with_different_special_characters(self):
        """Testa senha com diferentes caracteres especiais."""
        special_chars = '!@#$%^&*(),.?":{}|<>'

        for char in special_chars:
            password = f"Senha123{char}"
            # Não deve lançar exceção
            self.validator.validate(password)

    def test_validate_password_only_uppercase_and_lowercase(self):
        """Testa senha com apenas letras."""
        password = "SenhaApenas"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        # Deve falhar por falta de número
        assert exc_info.value.code == "password_no_number"

    def test_validate_password_multiple_missing_requirements(self):
        """Testa senha com múltiplos requisitos faltando."""
        # Sem maiúscula, sem número, sem especial
        password = "senhafraca"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        # Deve falhar no primeiro check (maiúscula)
        assert exc_info.value.code == "password_no_upper"

    def test_validate_password_only_special_and_numbers(self):
        """Testa senha com apenas números e caracteres especiais."""
        password = "123!@#456"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        # Deve falhar por falta de letra maiúscula
        assert exc_info.value.code == "password_no_upper"

    def test_validate_password_minimum_of_each_requirement(self):
        """Testa senha com apenas um de cada requisito."""
        password = "Aa1!"  # Maiúscula, minúscula, número, especial

        # Não deve lançar exceção - atende todos os requisitos do ComplexPasswordValidator
        # Mas pode falhar no Django por ser muito curta (mínimo 8 caracteres)
        self.validator.validate(password)

    def test_validate_password_with_spaces(self):
        """Testa senha com espaços."""
        password_with_spaces = "Senha Forte 123!"

        # Deve validar corretamente (espaços são permitidos)
        self.validator.validate(password_with_spaces)

    def test_validate_password_unicode_characters(self):
        """Testa senha com caracteres unicode."""
        password = "Sénhã123!"

        # Deve validar corretamente
        self.validator.validate(password)

    def test_get_help_text(self):
        """Testa o texto de ajuda do validador."""
        help_text = self.validator.get_help_text()

        assert "maiúscula" in help_text
        assert "minúscula" in help_text
        assert "número" in help_text
        assert "caractere especial" in help_text

    def test_validate_with_user_parameter(self):
        """Testa validação com parâmetro user (não usado mas aceito)."""
        password = "SenhaForte123!"

        # O parâmetro user é aceito mas não usado
        self.validator.validate(password, user=None)

    def test_validate_password_edge_cases(self):
        """Testa casos extremos de senha."""
        # Senha muito longa mas válida
        long_password = "A1!" + "a" * 100
        self.validator.validate(long_password)

        # Senha com todos os tipos de caracteres especiais
        complex_password = 'Abc123!@#$%^&*(),.?":{}|<>'
        self.validator.validate(complex_password)

    def test_validate_empty_password(self):
        """Testa senha vazia."""
        password = ""

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        assert exc_info.value.code == "password_no_upper"

    def test_validate_password_only_numbers(self):
        """Testa senha apenas com números."""
        password = "123456789"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        assert exc_info.value.code == "password_no_upper"

    def test_validate_password_mixed_case_numbers_no_special(self):
        """Testa senha com maiúsculas, minúsculas e números mas sem especial."""
        password = "SenhaForte123"

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate(password)

        assert exc_info.value.code == "password_no_symbol"
