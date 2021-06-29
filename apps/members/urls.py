from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("profile/", views.profile, name="profile"),
    path("membership/", views.view_membership, name="membership"),
    path("password/change/", views.password_change, name="password_change"),
    path("address/change/", views.ChangeAddress.as_view(), name="address_change"),
    path("login/", views.member_login, name="login"),
    path("logout/", views.member_logout, name="logout"),
]
