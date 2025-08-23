from dataclasses import dataclass #sirve para crear clases inmutables y con menos código
from datetime import datetime
from core.value_objects.email import Email


@dataclass
class User:
    id: int
    username: str
    email: Email
    password_hash: str
    created_at: datetime = datetime.now()

    def __post_init__(self):
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")

        if not isinstance(self.email, Email):
            raise TypeError("El email debe ser un objeto de tipo Email")

        if not self.password_hash:
            raise ValueError("El password hash no puede estar vacío")

    def check_password(self, raw_password: str, password_hasher) -> bool:
        """
        Verifica si la contraseña ingresada coincide con el hash almacenado.
        password_hasher es una dependencia inyectada (ej: werkzeug.security.check_password_hash)
        """
        return password_hasher(self.password_hash, raw_password)