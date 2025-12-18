"""
Funções úteis para validação e formatação.
"""

from django.core.exceptions import ValidationError


def validate_cpf(cpf: str) -> str:
    """
    Valida um CPF brasileiro.
    
    Args:
        cpf (str): CPF em formato string (apenas números)
    
    Returns:
        str: CPF validado
    
    Raises:
        ValidationError: Se o CPF for inválido
    
    Example:
        >>> validate_cpf("12345678909")
        "12345678909"
        >>> validate_cpf("11111111111")
        ValidationError: CPF inválido.
    """
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica tamanho
    if len(cpf) != 11:
        raise ValidationError("CPF deve conter 11 dígitos.")
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf in [str(n) * 11 for n in range(10)]:
        raise ValidationError("CPF inválido.")
    
    # Calcula primeiro dígito verificador
    calc = lambda t: int(t[1]) * (t[0] + 2)  # noqa: E731
    d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
    d1 = d1 if d1 < 10 else 0
    
    # Calcula segundo dígito verificador
    d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11
    d2 = d2 if d2 < 10 else 0
    
    # Verifica dígitos
    if not (d1 == int(cpf[-2]) and d2 == int(cpf[-1])):
        raise ValidationError("CPF inválido.")
    
    return cpf


def format_cpf(cpf: str) -> str:
    """
    Formata um CPF para o padrão XXX.XXX.XXX-XX.
    
    Args:
        cpf (str): CPF em formato string (apenas números ou com formatação)
    
    Returns:
        str: CPF formatado
    
    Example:
        >>> format_cpf("12345678909")
        "123.456.789-09"
    """
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Valida antes de formatar
    validate_cpf(cpf)
    
    # Formata
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validate_phone(phone: str) -> str:
    """
    Valida um número de telefone brasileiro.
    
    Args:
        phone (str): Telefone em formato string
    
    Returns:
        str: Telefone validado (apenas números)
    
    Raises:
        ValidationError: Se o telefone for inválido
    
    Example:
        >>> validate_phone("11999887766")
        "11999887766"
        >>> validate_phone("(11) 99988-7766")
        "11999887766"
    """
    # Remove caracteres não numéricos
    phone = ''.join(filter(str.isdigit, phone))
    
    # Verifica tamanho (10 ou 11 dígitos)
    if len(phone) not in [10, 11]:
        raise ValidationError("Telefone deve conter 10 ou 11 dígitos.")
    
    # Verifica se começa com DDD válido (código de área)
    ddd = int(phone[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError("DDD inválido.")
    
    return phone


def format_phone(phone: str) -> str:
    """
    Formata um número de telefone brasileiro.
    
    Args:
        phone (str): Telefone em formato string
    
    Returns:
        str: Telefone formatado
    
    Example:
        >>> format_phone("11999887766")
        "(11) 99988-7766"
        >>> format_phone("1133445566")
        "(11) 3344-5566"
    """
    # Remove caracteres não numéricos
    phone = ''.join(filter(str.isdigit, phone))
    
    # Valida antes de formatar
    validate_phone(phone)
    
    # Formata baseado no tamanho
    if len(phone) == 11:  # Celular com 9 dígitos
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    else:  # Fixo com 8 dígitos
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"


def sanitize_string(text: str, max_length: int = None) -> str:
    """
    Limpa e sanitiza uma string removendo espaços extras e caracteres especiais.
    
    Args:
        text (str): Texto a ser sanitizado
        max_length (int, optional): Comprimento máximo do texto
    
    Returns:
        str: Texto sanitizado
    
    Example:
        >>> sanitize_string("  Hello   World  ")
        "Hello World"
        >>> sanitize_string("Test", max_length=2)
        "Te"
    """
    if not text:
        return ""
    
    # Remove espaços extras
    text = " ".join(text.split())
    
    # Limita tamanho se especificado
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()
