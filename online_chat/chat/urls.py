# файл с путями сайта
from django.urls import path
from . import views
urlpatterns = [
    path("", views.HomeView.as_view(), name='start'),
    path("log/", views.LoginUserView.as_view(), name='log'),
    path("reg/", views.RegView.as_view(), name='reg'),
    path("log-out/", views.log_out, name='log-out'),
    path("chat-list/", views.ChatsView.as_view(), name='index'),
    path('chat/<str:chat_name>/', views.chat, name='chat'),
    path("create-chat/", views.ChatCreateView.as_view(), name="create-chat"),
    path("update-chat/<slug:chat_name>/", views.ChatUpdateView.as_view(), name="chat-up"),
    path("delete-chat/<slug:chat_name>/", views.ChatDeleteView.as_view(), name="delete-chat"),
    path("fix-chat/<slug:chat_name>/", views.ChatFixView.as_view(), name="fix-chat"),

]