from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import forms

app_name = 'members'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('join/', views.join, name='join'),
    path("profile/", views.profile, name="profile"),
    path("membership/", views.view_membership, name="membership"),
    path("password/change/", views.password_change, name="password_change"),
    path("login/", views.member_login, name="login"),
    path("logout/", views.member_logout, name="logout"),
]
