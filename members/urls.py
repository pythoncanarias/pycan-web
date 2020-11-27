from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('join/', views.join, name='join'),
    path("profile/", views.profile, name="profile"),
    path("login/", views.member_login, name="login"),
    path("logout/", views.member_logout, name="logout"),
]
