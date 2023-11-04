from django.urls import path, register_converter

from . import views


app_name = 'dashboard'


urlpatterns = [
    path('', views.index, name='index'),
    path('demo/', views.demo, name='demo'),
]
