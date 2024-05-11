import json
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Подключение
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.room_group_name = 'chat_%s' % self.chat_name

        # Присоединение к комнате группы WebSocket
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Отсоединение от комнаты группы WebSocket
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, **kwargs):
        # Приёмка сообщений через WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_name = text_data_json['chat_name']
        user_name = text_data_json['user']
        chat = Chat.objects.get(name=chat_name)
        user = User.objects.get(username=user_name)
        new_message = Message(user=user, words=message, chat=chat)
        new_message.save()
        time = timezone.now()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user_name,
                'time': time
            }
        )

    def chat_message(self, event):
        # Отправка сообщения клиенту через WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))




