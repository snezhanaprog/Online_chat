from django.db import models
from django.contrib.auth.models import User #импортируем модель пользователя

class Chat(models.Model): # модель чата
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # поле 'автор чата', связанное с моделью пользоваетеля первичным ключом
    name = models.CharField(max_length=20, unique=True) # строковое поле 'имя чата'
    text = models.TextField(null=True, blank=True, max_length=20) # текстовое поле 'краткое описание чата'
    date = models.DateTimeField(auto_now=True) # поле 'дата создания чата'
    fix = models.BooleanField(default=0) # булевое поле, указывающее на тип закрепления чата (чаты со значением 1 закреплены в списке пользователем, чаты со значением 0 не закреплены)

    class Meta:
        ordering = ['-date'] #сортировка чатов по дате

    def fixed(self):
        """
        метод для закрепления чата
        """
        if self.fix == 0:
            self.fix = 1
        else:
            self.fix = 0

class Message(models.Model): # модель сообщения
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # поле 'пользователь', связанное с моделью пользоваетеля первичным ключом
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True) # поле 'чат', связанное с моделью чата первичным ключом
    words = models.TextField(null=True) # текстовое поле 'содержание сообщения'
    date = models.DateTimeField(auto_now=True) # поле 'дата отправки сообщения'

    class Meta:
        ordering = ['-date']  #сортировка чатов по дате

    def user_name(self):
        return self.user

class Comment(models.Model): # модель комментария
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # поле 'автор комментария', связанное с моделью пользоваетеля первичным ключом
    words = models.TextField(null=True) # текстовое поле с содержанием комментария
    date = models.DateTimeField(auto_now=True) # поле 'дата отправки комментария'

    class Meta:
        ordering = ['-date']
