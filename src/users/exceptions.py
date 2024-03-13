from django.core.exceptions import ValidationError


class ImageSizeError(ValidationError):
    """Исключение, возникающее при превышении максимального размера."""


class ImageResizeError(Exception):
    """Исключение, возникающее при ошибке изменения размера изображения."""
