from django.urls import path, re_path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_member, name='new_member'),
    re_path(
        r'confirmation/(?P<encrypted_key>[\S]+)/', views.member_confirmation,
        name='member_confirmation'),
]
