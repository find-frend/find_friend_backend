import pytest


@pytest.fixture
def memory_channel_layers(settings):
    """Переопределяет конфигурацию слоёв каналов."""
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }


@pytest.fixture(autouse=True)
def null_logging(settings):
    """Переопределяет конфигурацию логирования."""
    settings.LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "null": {
                "class": "logging.NullHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["null"],
                "level": "CRITICAL",
                "propagate": False,
            },
        },
    }
