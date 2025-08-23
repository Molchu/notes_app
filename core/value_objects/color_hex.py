# core/value_objects/color_hex.py

from dataclasses import dataclass
from core.exceptions import DomainValidationError


@dataclass(frozen=True)
class ColorHex:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise DomainValidationError("El color debe ser una cadena")
        if not self.value.startswith("#") or len(self.value) != 7:
            raise DomainValidationError("Formato de color inválido. Use #RRGGBB")
        try:
            int(self.value[1:], 16)  # valida que los 6 caracteres sean hexadecimales
        except ValueError:
            raise DomainValidationError("El color debe ser un código HEX válido")

    def __str__(self):
        return self.value.upper()
