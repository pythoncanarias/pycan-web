from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('join/', views.join, name='join'),
    path('board', views.board, name='board'),
]
