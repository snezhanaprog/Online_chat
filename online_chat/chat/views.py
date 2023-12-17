from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UserForm

def start(request): # представление стартовой страницы
    return render(request, 'start.html')

def log(request): # представление страницы авторизации
    if request.method == 'POST':
        user_name = request.POST.get('user-name')
        password = request.POST.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') # поользователь авторизуется и попадает на страницу со списоком чатов
    return render(request, 'log.html')

def log_out(request): # представление выхода, перенаправляющее нас на стартовую страницу
    logout(request)
    return redirect('start')

def reg (request): # представление регистрации
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST) # заполнение формы
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            # регистрация после проверки данных
            #return redirect('index') # пользователь регистрируется и попадает на страницу со списоком чатов
    return render(request, 'reg.html', {'form' : form})


