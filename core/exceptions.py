class DomainError(Exception):
    """
    Excepción base para errores de dominio.
    Todas las demás deben heredar de aquí.
    """
    pass


class DomainValidationError(DomainError, ValueError):
    """
    Cuando una Entity o ValueObject no cumple sus invariantes.
    Ej: email inválido, título vacío, color mal formado.
    """
    pass


class EntityNotFoundError(DomainError, LookupError):
    """
    Cuando una entidad esperada no existe en el dominio.
    Ej: usuario no encontrado, nota inexistente.
    """
    pass


class PermissionDeniedError(DomainError, PermissionError):
    """
    Cuando un actor intenta realizar una acción sin autorización.
    Ej: usuario intenta editar una nota que no le pertenece.
    """
    pass