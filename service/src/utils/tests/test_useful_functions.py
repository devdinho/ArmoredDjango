"""
Testes para funções úteis de validação e formatação.
"""

import pytest
from django.core.exceptions import ValidationError

from utils.useful_functions import (
    format_cpf,
    format_phone,
    sanitize_string,
    validate_cpf,
    validate_phone,
)


class TestCPFValidation:
    """Testes para validação de CPF."""

    def test_validate_cpf_valid(self):
        """Testa validação de CPF válido."""
        # CPFs válidos para teste
        valid_cpfs = [
            "12345678909",
            "11144477735",
        ]

        for cpf in valid_cpfs:
            result = validate_cpf(cpf)
            assert result == cpf

    def test_validate_cpf_with_formatting(self):
        """Testa validação de CPF com formatação."""
        cpf_formatted = "123.456.789-09"
        result = validate_cpf(cpf_formatted)
        assert result == "12345678909"

    def test_validate_cpf_invalid_length(self):
        """Testa CPF com comprimento inválido."""
        with pytest.raises(ValidationError) as exc_info:
            validate_cpf("123456789")
        assert "11 dígitos" in str(exc_info.value)

    def test_validate_cpf_all_same_digits(self):
        """Testa CPF com todos dígitos iguais."""
        invalid_cpfs = ["11111111111", "00000000000", "99999999999"]

        for cpf in invalid_cpfs:
            with pytest.raises(ValidationError) as exc_info:
                validate_cpf(cpf)
            assert "inválido" in str(exc_info.value)

    def test_validate_cpf_invalid_check_digits(self):
        """Testa CPF com dígitos verificadores inválidos."""
        with pytest.raises(ValidationError) as exc_info:
            validate_cpf("12345678900")
        assert "inválido" in str(exc_info.value)

    def test_format_cpf(self):
        """Testa formatação de CPF."""
        cpf = "12345678909"
        formatted = format_cpf(cpf)
        assert formatted == "123.456.789-09"

    def test_format_cpf_already_formatted(self):
        """Testa formatação de CPF já formatado."""
        cpf = "123.456.789-09"
        formatted = format_cpf(cpf)
        assert formatted == "123.456.789-09"


class TestPhoneValidation:
    """Testes para validação de telefone."""

    def test_validate_phone_celular(self):
        """Testa validação de telefone celular (11 dígitos)."""
        phone = "11999887766"
        result = validate_phone(phone)
        assert result == phone

    def test_validate_phone_fixo(self):
        """Testa validação de telefone fixo (10 dígitos)."""
        phone = "1133445566"
        result = validate_phone(phone)
        assert result == phone

    def test_validate_phone_with_formatting(self):
        """Testa validação de telefone com formatação."""
        phone = "(11) 99988-7766"
        result = validate_phone(phone)
        assert result == "11999887766"

    def test_validate_phone_invalid_length(self):
        """Testa telefone com comprimento inválido."""
        with pytest.raises(ValidationError) as exc_info:
            validate_phone("123456789")
        assert "10 ou 11 dígitos" in str(exc_info.value)

    def test_validate_phone_invalid_ddd(self):
        """Testa telefone com DDD inválido."""
        with pytest.raises(ValidationError) as exc_info:
            validate_phone("09999887766")
        assert "DDD inválido" in str(exc_info.value)

    def test_format_phone_celular(self):
        """Testa formatação de telefone celular."""
        phone = "11999887766"
        formatted = format_phone(phone)
        assert formatted == "(11) 99988-7766"

    def test_format_phone_fixo(self):
        """Testa formatação de telefone fixo."""
        phone = "1133445566"
        formatted = format_phone(phone)
        assert formatted == "(11) 3344-5566"


class TestStringSanitization:
    """Testes para sanitização de strings."""

    def test_sanitize_string_extra_spaces(self):
        """Testa remoção de espaços extras."""
        text = "  Hello   World  "
        result = sanitize_string(text)
        assert result == "Hello World"

    def test_sanitize_string_max_length(self):
        """Testa limitação de comprimento."""
        text = "This is a long text"
        result = sanitize_string(text, max_length=10)
        assert result == "This is a "
        assert len(result) == 10

    def test_sanitize_string_empty(self):
        """Testa string vazia."""
        result = sanitize_string("")
        assert result == ""

    def test_sanitize_string_none(self):
        """Testa valor None."""
        result = sanitize_string(None)
        assert result == ""

    def test_sanitize_string_tabs_newlines(self):
        """Testa remoção de tabs e quebras de linha."""
        text = "Hello\t\nWorld\n\n"
        result = sanitize_string(text)
        assert result == "Hello World"
