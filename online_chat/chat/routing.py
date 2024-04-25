from django.urls import path
from . import consumers
print('12')
websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<chat_name>)\w+/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:chat_name>/', consumers.ChatConsumer.as_asgi()),
]
