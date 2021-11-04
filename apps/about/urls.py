from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('', views.index, name='index'),
    path('us/', views.us, name='us'),
    path('join/', views.join, name='join'),
    path('history/', views.history, name='history'),
    path('allies/', views.allies, name='allies'),
    path('faq/', views.faq_list, name='faq'),
]
