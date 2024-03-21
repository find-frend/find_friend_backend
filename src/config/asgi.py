"""
Настройки ASGI сервера.

<=!!! ВНИМАНИЕ! ПОРЯДОК ИМПОРТОВ И СТРОК КОДА ВАЖЕН И НЕ ДОЛЖЕН МЕНЯТЬСЯ !!!=>

Необходимо инициализировать приложение Djando ASGI как можно раньше,
чтобы AppRegistry был заполнен до того, как последующие импорты
повлекут за собой импорт ORM моделей.
"""

from django.core.asgi import get_asgi_application  # noqa

django_asgi_app = get_asgi_application()  # noqa

import os  # noqa

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa

from chat import routing  # noqa
from chat.middleware import TokenAuthMiddleware  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
