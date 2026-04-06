# base
class AppError(Exception):
    "Базовое приложение исключение"
    pass


# 4 ключевых категории

class NotFoundError(AppError):
    "Сущность не найдена"
    pass


class ValidationError(AppError):
    "Ошибка валидации входных данных"
    pass


class AlreadyExistsError(AppError):
    "Конфликт уникальности / уже существует"
    pass


class DatabaseError(AppError):
    "Любая непредвиденная ошибка БД"
    pass