import functools
import logging

from config import settings

logger = logging.getLogger(settings.CUSTOM_LOGGER_NAME)


class NameUpperFilter(logging.Filter):
    """Фильтр для добавления имени логгера в верхнем регистре."""

    def filter(self, record):
        """Метод фильтрации."""
        record.name_upper = record.name.split(".")[0].upper()
        return True


def get_level(level):
    """Получение уровня логирования."""
    if isinstance(level, int):
        return level
    lvl = logging.getLevelName(level)
    if isinstance(lvl, int):
        return lvl
    return logging.DEBUG


def log(level=logging.DEBUG, logger=logger):
    """Декоратор, логирующий аргументы функции и возвращаемые значения."""

    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            lvl = get_level(level)
            logger.log(
                lvl,
                f"Функция {func.__name__} модуля {func.__module__} "
                f"вызвана с аргументами {signature}.",
            )
            try:
                result = func(*args, **kwargs)
                logger.log(
                    lvl,
                    f"Функция {func.__name__} модуля {func.__module__} "
                    f"вернула: {result}",
                )
                return result
            except Exception as e:
                logger.exception(
                    f"В функции {func.__name__} модуля {func.__module__} "
                    f"вызвано исключение: {str(e)}"
                )
                raise e

        return wrapper

    return decorator_log
