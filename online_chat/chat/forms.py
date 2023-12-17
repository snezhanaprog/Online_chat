from django import forms
from django.contrib.auth.models import User # импортируем модель пользователя

class UserForm(forms.ModelForm):
    # форма регистации пользователя
    password = forms.CharField( widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email')