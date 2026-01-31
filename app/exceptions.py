# app/exceptions.py
"""
Custom exception classes for consistent error handling across the API.
"""
from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """Raised when a requested resource is not found."""
    def __init__(self, entity: str, identifier: any = None):
        detail = f"{entity} not found"
        if identifier is not None:
            detail = f"{entity} not found: {identifier}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenError(HTTPException):
    """Raised when user lacks permission for an action."""
    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestError(HTTPException):
    """Raised when the request is invalid."""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedError(HTTPException):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ConflictError(HTTPException):
    """Raised when there's a conflict with current state."""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
