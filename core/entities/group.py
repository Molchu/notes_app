# core/entities/group.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.exceptions import DomainValidationError

MAX_NAME_LEN = 80
MAX_DESC_LEN = 500


@dataclass
class Group:
    id: int
    user_id: int               # referencia al usuario que creó el grupo
    name: str
    description: Optional[str] = None
    color: Optional[str] = None  # HEX opcional (#RRGGBB). Si lo deseas, usar ValueObject ColorHex
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # --- Validaciones ---
    def __post_init__(self):
        self._validate_name(self.name)

        if self.description:
            self._validate_description(self.description)

        if self.color and not self._is_valid_hex(self.color):
            raise DomainValidationError("El color debe ser un HEX válido (#RRGGBB)")

        if self.user_id <= 0:
            raise DomainValidationError("user_id inválido")

    # --- Comportamientos de dominio ---
    def rename(self, new_name: str) -> None:
        self._validate_name(new_name)
        self.name = new_name.strip()
        self._touch()

    def update_description(self, new_desc: Optional[str]) -> None:
        if new_desc:
            self._validate_description(new_desc)
        self.description = new_desc
        self._touch()

    def change_color(self, new_color: Optional[str]) -> None:
        if new_color and not self._is_valid_hex(new_color):
            raise DomainValidationError("El color debe ser un HEX válido (#RRGGBB)")
        self.color = new_color
        self._touch()

    # --- Helpers internos ---
    def _touch(self) -> None:
        self.updated_at = datetime.now()

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise DomainValidationError("El nombre del grupo no puede estar vacío")
        if len(name.strip()) > MAX_NAME_LEN:
            raise DomainValidationError(f"El nombre del grupo no puede exceder {MAX_NAME_LEN} caracteres")

    @staticmethod
    def _validate_description(desc: str) -> None:
        if len(desc.strip()) > MAX_DESC_LEN:
            raise DomainValidationError(f"La descripción no puede exceder {MAX_DESC_LEN} caracteres")

    @staticmethod
    def _is_valid_hex(value: str) -> bool:
        if not isinstance(value, str) or not value.startswith("#") or len(value) != 7:
            return False
        try:
            int(value[1:], 16)
            return True
        except ValueError:
            return False
