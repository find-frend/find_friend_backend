import pytest
from channels.testing import WebsocketCommunicator

from config.asgi import application


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestWebSocket:
    """Тесты для WebSocket."""

    async def test_can_connect_to_server(
        self, chat, token, memory_channel_layers
    ):
        """Проверка подключения к серверу."""
        url_chat = f"/ws/chat/{chat.id}/"
        token_bytes = token.encode("utf-8")
        communicator = WebsocketCommunicator(
            application=application,
            path=url_chat,
            headers=[(b"authorization", b"Token " + token_bytes)],
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()
