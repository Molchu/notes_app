from core.exceptions import DomainError
from application.interfaces.user_repository import UserRepository


class LoginUser:
    def __init__(self, user_repo: UserRepository, password_checker):
        self.user_repo = user_repo
        self.password_checker = password_checker

    def execute(self, email: str, raw_password: str):
        user = self.user_repo.get_by_email(email)
        if not user:
            raise DomainError("Usuario no encontrado")

        if not user.check_password(raw_password, self.password_checker):
            raise DomainError("Contraseña inválida")

        return user
