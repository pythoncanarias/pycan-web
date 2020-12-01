from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('versions/', views.versions, name='versions'),
]
