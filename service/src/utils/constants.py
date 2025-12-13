class ProfileType(object):
    """Object representando diferentes tipos de Perfis de Usuários.

    Atributos:
        - ADMIN (int): Administrador, usuário com permissões de Administrador.
        - DEVELOPER (int): Desenvolvedor, usuário com permissões de Desenvolvedor.
        - EARUSER (int): Usuário Padrão, usuário com permissões de Usuário Padrão.
    """

    ADMIN = 1
    DEVELOPER = 2
    EARUSER = 3

    PROFILE_TYPE_CHOICES = (
        (ADMIN, "Administrador"),
        (DEVELOPER, "Desenvolvedor"),
        (EARUSER, "Usuário Padrão"),
    )


class EmailType(object):
    """Object representando diferentes tipos de Emails.

    Atributos:
        - WELCOME (int): Email de Boas Vindas.
        - PASSWORD_RESET (int): Email de Redefinição de Senha.
        - NOTIFICATION (int): Email de Notificação.
    """

    WELCOME = 1
    PASSWORD_RESET = 2
    NOTIFICATION = 3

    EMAIL_TYPE_CHOICES = (
        (WELCOME, "Boas Vindas"),
        (PASSWORD_RESET, "Redefinição de Senha"),
        (NOTIFICATION, "Notificação"),
    )
