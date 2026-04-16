"""Domain exceptions.

Services raise these; routers catch and translate to HTTP responses.
Never use HTTPException outside of routers.
"""


class BraslinaError(Exception):
    """Base for all domain errors."""

    def __init__(self, message: str = "", code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(BraslinaError):
    """Entity not found."""

    def __init__(self, entity: str, entity_id: str):
        super().__init__(
            message=f"{entity} '{entity_id}' not found",
            code="NOT_FOUND",
        )
        self.entity = entity
        self.entity_id = entity_id


class InvalidStateTransition(BraslinaError):
    """Illegal status change."""

    def __init__(self, entity: str, current: str, target: str):
        super().__init__(
            message=f"{entity}: transition {current} -> {target} not allowed",
            code="INVALID_STATE_TRANSITION",
        )


class ValidationError(BraslinaError):
    """Business-rule validation failure."""

    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR")


class DuplicateError(BraslinaError):
    """Duplicate entity / idempotency conflict."""

    def __init__(self, message: str):
        super().__init__(message=message, code="DUPLICATE")
