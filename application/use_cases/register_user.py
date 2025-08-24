from core.entities.user import User
from core.value_objects.email import Email
from core.exceptions import DomainError
from application.interfaces.user_repository import UserRepository


class RegisterUser:
    def __init__(self, user_repo: UserRepository, password_hasher):
        """
        :param user_repo: implementación concreta del repositorio de usuarios (inyectado).
        :param password_hasher: función/servicio para generar hash de la contraseña.
        """
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, username: str, email: str, raw_password: str) -> User:
        # Validar email con value object
        email_vo = Email(email)

        # Verificar que no exista ya
        if self.user_repo.get_by_email(email_vo):
            raise DomainError("El usuario ya existe con ese correo")

        # Hash de contraseña
        hashed_pw = self.password_hasher(raw_password)

        # Crear entidad
        user = User(id=None, username=username, email=email_vo, password_hash=hashed_pw)

        # Guardar en repo
        return self.user_repo.add(user)
