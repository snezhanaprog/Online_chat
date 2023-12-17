# файл с путями сайта
from django.urls import path
from . import views
urlpatterns = [
    path("", views.start, name='start'),
    path("log/", views.log, name='log'),
    path("reg/", views.reg, name='reg'),
    path("log-out/", views.log_out, name='log-out'),

]