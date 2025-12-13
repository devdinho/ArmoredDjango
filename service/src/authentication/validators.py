import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """
    Valida se a senha contém pelo menos:
    - 1 letra maiúscula
    - 1 letra minúscula
    - 1 número
    - 1 caractere especial
    """

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra maiúscula."),
                code="password_no_upper",
            )

        if not any(char.islower() for char in password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra minúscula."),
                code="password_no_lower",
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("A senha deve conter pelo menos um número."),
                code="password_no_number",
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um caractere especial."),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos uma letra maiúscula, "
            "uma minúscula, um número e um caractere especial."
        )
