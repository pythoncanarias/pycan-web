from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join, name='join'),
    path('history/', views.history, name='history'),
]
