from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.exceptions import DomainValidationError
from core.value_objects.color_hex import ColorHex, DEFAULT_NOTE_COLOR  # lo crearemos en value_objects
# Si aún no tienes ColorHex, temporalmente puedes usar Optional[str] y validar luego.


MAX_TITLE_LEN = 120 # título no puede exceder 120 caracteres
MAX_CONTENT_LEN = 20_000 # contenido no puede exceder 20,000 caracteres


@dataclass
class Note:
    id: int
    user_id: int                      # referencia al usuario (dominio, no ORM)
    title: str
    content: str
    color: Optional[ColorHex | str] = None  # Value Object para color HEX (#RRGGBB)
    group_id: Optional[int] = None     # permite agrupar notas
    is_archived: bool = False
    is_pinned: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # --- Validaciones de invariante de la Entidad ---
    def __post_init__(self):
        self._validate_title(self.title)
        self._validate_content(self.content)

        if self.color is None:
            self.color = DEFAULT_NOTE_COLOR

        if self.user_id <= 0:
            raise DomainValidationError("user_id inválido")

        if self.group_id is not None and self.group_id <= 0:
            raise DomainValidationError("group_id inválido")

    # --- Comportamientos de dominio (no dependen de frameworks) ---
    def rename(self, new_title: str) -> None:
        self._validate_title(new_title)
        self.title = new_title.strip()
        self._touch()

    def update_content(self, new_content: str) -> None:
        self._validate_content(new_content)
        self.content = new_content
        self._touch()

    def change_color(self, new_color: Optional[ColorHex]) -> None:
        # Permite quitar color (None) o asignar uno válido
        if new_color is not None and not isinstance(new_color, ColorHex):
            raise DomainValidationError("color debe ser un ColorHex válido")
        self.color = new_color
        self._touch()

    def move_to_group(self, new_group_id: Optional[int]) -> None:
        # None = sin grupo
        if new_group_id is not None and new_group_id <= 0:
            raise DomainValidationError("group_id inválido")
        self.group_id = new_group_id
        self._touch()

    def pin(self) -> None:
        self.is_pinned = True
        self._touch()

    def unpin(self) -> None:
        self.is_pinned = False
        self._touch()

    def archive(self) -> None:
        self.is_archived = True
        self._touch()

    def unarchive(self) -> None:
        self.is_archived = False
        self._touch()

    def preview(self, max_chars: int = 120) -> str:
        """
        Retorna un resumen de contenido para listados.
        """
        snippet = (self.content or "").strip().replace("\n", " ")
        return snippet[:max_chars] + ("…" if len(snippet) > max_chars else "")

    # --- Helpers internos ---
    def _touch(self) -> None:
        self.updated_at = datetime.now()

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title or not title.strip():
            raise DomainValidationError("El título no puede estar vacío")
        if len(title.strip()) > MAX_TITLE_LEN:
            raise DomainValidationError(f"El título no puede exceder {MAX_TITLE_LEN} caracteres")

    @staticmethod
    def _validate_content(content: str) -> None:
        if content is None:
            raise DomainValidationError("El contenido no puede ser None")
        if len(content) > MAX_CONTENT_LEN:
            raise DomainValidationError(f"El contenido no puede exceder {MAX_CONTENT_LEN} caracteres")