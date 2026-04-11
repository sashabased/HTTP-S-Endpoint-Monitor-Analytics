# base
class AppError(Exception):
    """Base app exception"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# 4 ключевых категории

class NotFoundError(AppError):
    """Entity not found"""
    pass


class ValidationError(AppError):
    """Validation error on new data"""
    pass


class AlreadyExistsError(AppError):
    """Unique conflict / already exists"""
    pass


class DatabaseError(AppError):
    """Any database error"""
    pass