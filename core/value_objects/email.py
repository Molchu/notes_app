# core/value_objects/email.py

from __future__ import annotations
from dataclasses import dataclass
import re

from core.exceptions import DomainValidationError


# Regex pragmática (no intenta cubrir todo RFC 5322, pero es segura para app web)
# - Local part: caracteres comunes permitidos
# - Dominio: al menos un punto; etiquetas alfanuméricas separadas por puntos
_EMAIL_RE = re.compile(
    r"^(?P<local>[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)$"
)

MAX_EMAIL_LEN = 254
MAX_LOCAL_LEN = 64


@dataclass(frozen=True)
class Email:
    """
    Value Object inmutable que representa un email válido.
    - Normaliza: trim y lowercase completo
    - Valida: longitud, formato, dominio y etiquetas
    """
    value: str

    def __post_init__(self):
        raw = (self.value or "").strip()
        if not raw:
            raise DomainValidationError("El email no puede estar vacío")

        # Normalización: todo a minúsculas (la mayoría de sistemas tratan el local-part case-insensitive)
        norm = raw.lower()

        if len(norm) > MAX_EMAIL_LEN:
            raise DomainValidationError("El email excede la longitud máxima permitida")

        m = _EMAIL_RE.match(norm)
        if not m:
            raise DomainValidationError("Formato de email inválido")

        local = m.group("local")
        domain = m.group("domain")

        if len(local) > MAX_LOCAL_LEN:
            raise DomainValidationError("La parte local del email excede 64 caracteres")

        # Reglas simples adicionales
        if ".." in local or ".." in domain:
            raise DomainValidationError("El email no puede contener puntos consecutivos")

        # Validar etiquetas del dominio (sin guiones al inicio/fin)
        for label in domain.split("."):
            if not label or label.startswith("-") or label.endswith("-"):
                raise DomainValidationError("Etiqueta de dominio inválida en el email")

        # TLD con al menos 2 caracteres
        tld = domain.split(".")[-1]
        if len(tld) < 2:
            raise DomainValidationError("El dominio debe tener un TLD válido")

        # Congelar con el valor normalizado
        object.__setattr__(self, "value", norm)

    # ---- Helpers de conveniencia (no mutan estado) ----
    @property
    def local(self) -> str:
        return self.value.split("@", 1)[0]

    @property
    def domain(self) -> str:
        return self.value.split("@", 1)[1]

    def masked(self) -> str:
        """
        Devuelve una versión ofuscada para logs: ju****@dominio.com
        """
        l = self.local
        if len(l) <= 2:
            lmask = "*" * len(l)
        else:
            lmask = l[:2] + "*" * (len(l) - 2)
        return f"{lmask}@{self.domain}"

    def __str__(self) -> str:
        return self.value
