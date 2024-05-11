from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.views import View


class HomeView(View):
    template_name = 'start.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginUserView(View):
    template_name = 'log.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_name = request.POST.get('name') # получаем имя пользователя
        password = request.POST.get('password') # получаем пароль пользователя
        print(user_name, password)
        user = authenticate(request, username=user_name, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        return redirect('log')


def log_out(request):
    logout(request)
    return redirect('start')


class RegView(CreateView):
    template_name = 'reg.html'

    success_url = reverse_lazy('index')
    form_class = UserForm

    def form_valid(self, form):
        # Этот метод вызывается, когда валидация формы прошла успешно.
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)  # Выполняем вход для пользователя после регистрации
        return super().form_valid(form)


class ChatsView(LoginRequiredMixin, ListView):
    # представление списка чатов
    template_name = 'index.html'
    context_object_name = 'chats'
    model = Chat
    login_url = 'log'

    def get_queryset(self):
        req = self.request.GET.get('find', '')
        if req.startswith('#') and req[1:].isnumeric():
            # ищем по id чата
            return Chat.objects.filter(id=int(req[1:]))
        elif req:
            # ищем по названию чата
            return Chat.objects.filter(name__icontains=req)
        else:
            # показываем все незакреплённые чаты
            return Chat.objects.filter(fix=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['find'] = self.request.GET.get('find', '')
        if context['find'] == '':
            context['fix'] = Chat.objects.filter(fix=1)  # закреплённые чаты
        else:
            context['fix'] = None
        return context


class ChatView(LoginRequiredMixin, DetailView):
    login_url = 'log'
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'chat'
    slug_field = 'name'
    slug_url_kwarg = 'chat_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        chat = context['chat']
        context['messages'] = Message.objects.filter(chat=chat)


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


class ChatUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'log'
    slug_field = 'name'
    slug_url_kwarg = 'chat_name'
    template_name = 'create-chat.html'
    success_url = reverse_lazy('index')
    model = Chat
    fields = ['name', 'text']

    def get_object(self, queryset=None):
        chat_name = self.kwargs.get('chat_name')
        return get_object_or_404(Chat, name=chat_name)


class ChatCreateView(LoginRequiredMixin, CreateView):
    login_url = 'log'
    template_name = 'create-chat.html'
    success_url = reverse_lazy('index')
    model = Chat
    fields = ['name', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Задаем автора чата текущим пользователем
        return super(ChatCreateView, self).form_valid(form)


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete-chat.html'
    model = Chat
    context_object_name = 'chat'
    slug_field = 'name'
    slug_url_kwarg = 'chat_name'
    login_url = 'log'
    success_url = reverse_lazy('index')

    def get_object(self, query_set=None):
        chat_name = self.kwargs['chat_name']
        return get_object_or_404(Chat, name=chat_name)


class ChatFixView(LoginRequiredMixin, View):
    template_name = 'fix-chat.html'
    login_url = 'log'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        chat_name = self.kwargs['chat_name']
        chat = get_object_or_404(Chat, name=chat_name)
        msg = 'Открепить' if chat.fix else 'Закрепить'
        return render(request, self.template_name, {'chat': chat, 'msg': msg})

    def post(self, request, *args, **kwargs):
        chat_name = self.kwargs.get('chat_name')
        chat = get_object_or_404(Chat, name=chat_name)
        chat.fixed()
        chat.save()
        return redirect(self.success_url)
