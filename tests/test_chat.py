import pytest
from asgiref.sync import sync_to_async

from chat.models import Message
from chat.serializers import MessageSerializer


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestWebSocket:
    """Тесты для WebSocket."""

    async def test_can_connect_to_server(
        self,
        create_ws_communicator,
        chat,
        create_token,
        user,
        memory_channel_layers,
    ):
        """Проверка подключения к серверу."""
        token = await sync_to_async(create_token)(user)
        ws_communicator = create_ws_communicator(chat, token)
        connected, _ = await ws_communicator.connect()
        assert connected
        await ws_communicator.disconnect()

    async def test_cannot_connect_to_server_if_unfriended(
        self,
        create_ws_communicator,
        chat_ufriended,
        create_token,
        user,
        memory_channel_layers,
    ):
        """Если пользователи больше не друзья, подключение невозможно."""
        token = await sync_to_async(create_token)(user)
        ws_communicator = create_ws_communicator(chat_ufriended, token)
        connected, _ = await ws_communicator.connect()
        assert not connected
        await ws_communicator.disconnect()

    async def test_cannot_connect_to_chat_if_not_member(
        self,
        create_ws_communicator,
        chat,
        create_token,
        third_user,
        memory_channel_layers,
    ):
        """Если пользователь не состоит в чате, подключение невозможно."""
        token = await sync_to_async(create_token)(third_user)
        ws_communicator = create_ws_communicator(chat, token)
        connected, _ = await ws_communicator.connect()
        assert not connected
        await ws_communicator.disconnect()

    async def test_anonymous_user_cannot_connect_to_chat(
        self, ws_communicator_anonymous, memory_channel_layers
    ):
        """Анонимный пользователь не может подключиться к чату."""
        connected, _ = await ws_communicator_anonymous.connect()
        assert not connected
        await ws_communicator_anonymous.disconnect()

    async def test_message_exchange_between_users(
        self, ws_connection, another_ws_connection, memory_channel_layers
    ):
        """Обмен сообщениями между пользователями в чате."""
        # Пользователь 1 отправляет сообщение простым текстом
        await ws_connection.send_to("Test message from User 1")

        # Пользователь 2 получает сообщение в виде JSON (объект сообщения)
        response = await another_ws_connection.receive_json_from()
        for field in list(MessageSerializer().get_fields().keys()):
            assert field in response
        # Текст в JSON соответствует отправленному тексту
        assert response["text"] == "Test message from User 1"

        # Сообщение должно сохраниться в базе
        messages_in_db = await sync_to_async(list)(Message.objects.all())
        assert len(messages_in_db) == 1
