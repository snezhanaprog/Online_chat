# файл с путями сайта
from django.urls import path
from . import views
urlpatterns = [
    path("", views.start, name='start'),
    path("log/", views.log, name='log'),
    path("reg/", views.reg, name='reg'),
    path("log-out/", views.log_out, name='log-out'),
    path("chat-list/", views.index, name='index'),
    path('chat/<str:chat_name>/', views.chat, name='chat'),
    path("create-chat/", views.create_chat, name="create-chat"),
    path("update-chat/<str:chat_name>/", views.chat_up, name="chat-up"),
    path("delete-chat/<str:chat_name>/", views.del_chat, name="delete-chat"),
    path("fix-chat/<str:chat_name>/", views.fix_chat, name="fix-chat"),

]