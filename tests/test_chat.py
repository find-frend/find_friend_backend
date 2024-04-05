from http import HTTPStatus

import pytest
from asgiref.sync import sync_to_async

from chat.models import Chat, Message  # noqa
from chat.serializers import MessageSerializer


@pytest.mark.django_db(transaction=True)
class TestChatHTTP:
    """Тесты чатов - HTTP."""

    start_chat_url = "/api/v1/chats/start/"
    view_chat_url = "/api/v1/chats/%d/"
    list_chats_url = "/api/v1/chats/"

    def test_friends_can_start_chat(self, user_client, friends):
        """Друзья могут создать чат."""
        response = user_client.post(
            self.start_chat_url, data={"email": friends.friend.email}
        )

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"Страница `{self.start_chat_url}` не найдена, "
            "проверьте этот адрес в *urls.py*"
        )

        assert (
            response.status_code == HTTPStatus.OK
        ), f"Страница `{self.start_chat_url}` работает неправильно!"

        chat_created_data = response.json()
        assert all(
            field in chat_created_data
            for field in ["initiator", "receiver", "chat_messages"]
        ), (
            f"Проверьте, что при POST запросе на `{self.start_chat_url}` "
            "возвращается объект xчата."
        )

    def test_strangers_cannot_start_chat(self, user, third_user):
        """Пользователи, не состоящие в друзьях, не могут создать чат."""
        pass

    def test_cannot_start_chat_with_nonexistent_user(self, user):
        """Нельзя создать чат с несуществующим пользователем."""
        pass

    def start_existing_chat(self, user, another_user):
        """Попытка создания чата, который уже существует."""
        pass

    def test_anonymous_user_cannot_view_chat(self, user, another_user):
        """Анонимный пользователь не может просматривать чат."""
        pass

    def test_non_members_cannot_view_chat(self, user, another_user):
        """Пользователи, не состоящие в чате, не могут просматривать чат."""
        pass

    def test_user_can_list_only_their_chats(self, user, another_user):
        """Пользователь может просматривать только свои чаты."""
        pass

    def test_chat_view_contains_limited_amount_of_messages(
        self, user, another_user
    ):
        """Просмотр чата содержит ограниченное количество сообщений."""
        pass

    def test_chat_remains_after_user_deleted(self, user, another_user):
        """Чат остается после удаления пользователя."""
        pass

    def test_chat_messages_remain_after_user_deleted(self, user, another_user):
        """Сообщения остаются после удаления пользователя."""
        pass


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestChatWebSocket:
    """Тесты чатов - WebSocket."""

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
        # Поля в JSON соответствуют полям в сериализаторе
        for field in list(MessageSerializer().get_fields().keys()):
            assert field in response
        # Текст сообщения в JSON соответствует отправленному тексту
        assert response["text"] == "Test message from User 1"

        # Сообщение должно сохраниться в базе
        messages_in_db = await sync_to_async(list)(Message.objects.all())
        assert len(messages_in_db) == 1
