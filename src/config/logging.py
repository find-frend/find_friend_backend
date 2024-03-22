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


def log(logger=logger):
    """Декоратор, логирующий аргументы функции и возвращаемые значения."""

    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            print(logger)
            print(type(logger))
            logger.debug(
                f"Функция {func.__name__} вызвана с аргументами {signature}."
            )
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Функция {func.__name__} вернула: {result}")
                return result
            except Exception as e:
                logger.exception(
                    f"В функции {func.__name__} вызвано исключение: {str(e)}"
                )
                raise e

        return wrapper

    return decorator_log
