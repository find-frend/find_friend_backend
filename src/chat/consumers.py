import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Chat, Message
from chat.serializers import MessageSerializer
from config.settings import MAX_MESSAGES_IN_CHAT


class ChatConsumer(WebsocketConsumer):
    """Consumer для чатов."""

    def connect(self):
        """Подключение к чату."""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # Подгрузка последних X сообщений
        messages = Message.objects.filter(chat=int(self.room_name)).order_by(
            "-timestamp"
        )[:MAX_MESSAGES_IN_CHAT]
        self.send_messages(messages)

    def disconnect(self, close_code):
        """Отключение от чата."""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        """Получение сообщения от вебсокета."""
        chat = Chat.objects.get(id=int(self.room_name))
        sender = self.scope["user"]

        message_obj = Message.objects.create(
            sender=sender,
            text=text_data,
            chat=chat,
        )

        serializer = MessageSerializer(instance=message_obj)

        # Send message to room group
        chat_type = {"type": "chat_message"}
        message = {"message": {**serializer.data}}
        return_dict = {**chat_type, **message}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):
        """Получение сообщения от чата."""
        text_data_json = event.copy()
        text_data_json.pop("type")
        message = text_data_json["message"]

        self.send(text_data=json.dumps(message))

    def send_messages(self, messages):
        """Отправка нескольких сообщений на вебсокет."""
        for message in messages:
            serializer = MessageSerializer(instance=message)
            self.send(text_data=json.dumps(serializer.data))
