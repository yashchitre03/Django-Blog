from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
    For generating the token for account actication.
    """
    pass


account_activation_token = TokenGenerator()
