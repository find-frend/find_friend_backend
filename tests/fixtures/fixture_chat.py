import pytest
import pytest_asyncio
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from chat.models import Chat, Message
from config.asgi import application
from config.constants import MAX_MESSAGES_IN_CHAT
from users.models import Friendship


@pytest.fixture
def chat(db, friends):
    """Тестовый чат."""
    return Chat.objects.create(
        initiator=friends.initiator, receiver=friends.friend
    )


@pytest.fixture
def many_messages(user, chat):
    """Создание множества сообщений."""
    messages = []
    text_template = "Message{}"
    for i in range(MAX_MESSAGES_IN_CHAT + 1):
        sender = user
        chat_instance = chat
        text = text_template.format(i)
        message = Message(sender=sender, chat=chat_instance, text=text)
        messages.append(message)
    Message.objects.bulk_create(messages)
    return messages


@pytest.fixture
def chat_ufriended(db, user, third_user):
    """Чат без дружбы."""
    friendship = Friendship.objects.create(initiator=user, friend=third_user)
    chat = Chat.objects.create(initiator=user, receiver=third_user)
    friendship.delete()
    return chat  # noqa


@pytest.fixture
def ws_communicator_anonymous(db, chat, event_loop):
    """Объект WebSocket коммуникатора для анонимного пользователя."""
    url_chat = f"/ws/chat/{chat.id}/"
    communicator = WebsocketCommunicator(
        application=application,
        path=url_chat,
    )
    # Reset server task to prevent cancellation issues
    communicator._server_task = None
    # Set the event loop
    communicator._event_loop = event_loop
    return communicator


@pytest.fixture
def create_ws_communicator(db, event_loop):
    """Фабрика создания объекта WebSocket коммуникатора."""

    def _create_ws_communicator(_chat, _token):
        url_chat = f"/ws/chat/{_chat.id}/"
        token_bytes = _token.encode("utf-8")
        communicator = WebsocketCommunicator(
            application=application,
            path=url_chat,
            headers=[(b"authorization", b"Token " + token_bytes)],
        )
        # Reset server task to prevent cancellation issues
        communicator._server_task = None
        # Set the event loop
        communicator._event_loop = event_loop
        return communicator

    return _create_ws_communicator


@pytest_asyncio.fixture
async def ws_connection(
    create_ws_communicator, chat, create_token, user, memory_channel_layers
):
    """Фикстура WebSocket подключения со стороны пользователя user."""
    token = await sync_to_async(create_token)(user)
    ws_communicator = create_ws_communicator(chat, token)
    await ws_communicator.connect()
    try:
        yield ws_communicator
    finally:
        await ws_communicator.disconnect()


@pytest_asyncio.fixture
async def another_ws_connection(
    create_ws_communicator,
    chat,
    create_token,
    another_user,
    memory_channel_layers,
):
    """Фикстура WebSocket подключения со стороны пользователя another_user."""
    token = await sync_to_async(create_token)(another_user)
    ws_communicator = create_ws_communicator(chat, token)
    await ws_communicator.connect()
    try:
        yield ws_communicator
    finally:
        await ws_communicator.disconnect()
