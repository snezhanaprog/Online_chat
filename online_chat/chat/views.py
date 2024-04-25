from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import Chat, Message

def start(request): # представление стартовой страницы
    return render(request, 'start.html')

def log(request): # представление страницы авторизации
    if request.method == 'POST':
        user_name = request.POST.get('name') # получаем имя пользователя
        password = request.POST.get('password') # получаем пароль пользователя
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
        print('0')
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            print('1')
            # регистрация после проверки данных
            return redirect('index') # пользователь регистрируется и попадает на страницу со списоком чатов
    return render(request, 'reg.html', {'form': form})

@login_required(login_url='log')
def index(request): #представление списка чатов
    #req = request.Get.get('find') # проверяем посиковую строку
    req = None
    fix = Chat.objects.filter(fix=1)  # закреплённые чаты
    chats = Chat.objects.filter(fix=0)  # незакреплённые чаты
    if req != None: # если строка не пустая, ищем чат
        if req[1:].isnumeric() and req[:1] == '#':
            # ищем по id чата
            find = int(req[1:])
            chats = Chat.objects.filter(id=find) # получаем список чатов для вывода
        else:
            # ищем по названию чата
            find = request.GET.get('find')
            chats = Chat.objects.filter(name__icontains=find) # получаем список чатов для вывода
    else:
        # поисковая строка пуста, значит показываем все чаты
        find = ''
    context = {'chats':chats,
               'find':find,
               'fix':fix}
    return render(request,'index.html', context)

@login_required(login_url='log')
def chat(request, chat_name):
    chat = get_object_or_404(Chat, name=chat_name)
    messages = Message.objects.filter(chat=chat)
    context = {
        "messages": messages,
        "user": request.user,
        "chat": chat,
        "chat_name": chat_name
    }
    return render(request, 'chat.html', context)

@login_required(login_url='log')
def chat_up(request, chat_name): #представление редактирования чата
    chat = Chat.objects.get(name=chat_name)
    if request.method == 'POST':
        chat.name = request.POST.get('name')
        chat.text = request.POST.get('text')
        chat.save()
        return redirect('index')
    return render(request, 'create-chat.html')

@login_required(login_url='log')
def create_chat(request):
    # представление создания чата
    if request.method == 'POST':
        chat = Chat.objects.create(
            author=request.user,
            name=request.POST.get('name'),
            text=request.POST.get('text'),
            fix=0
        )
        return redirect('index')
    return render(request, 'create-chat.html')

@login_required(login_url='log')
def del_chat(request, chat_name): #представление удаления чата
    chat = Chat.objects.get(name=chat_name)
    if request.method == 'POST':
        chat.delete()
        return redirect('index')
    return render(request, 'delete-chat.html', {'chat':chat})

@login_required(login_url='log')
def fix_chat(request, chat_name): #представление закрепления чата
    chat = Chat.objects.get(name=chat_name)
    if chat.fix == 0:
        msg = 'Закрепить'
    else:
        msg = 'Открепить'
    if request.method == 'POST':
        chat.fixed()
        chat.save()
        return redirect('index')
    return render(request, 'fix-chat.html', {'chat':chat, 'msg':msg})


