from django.urls import include, path
from . import views

from . import models

urlpatterns = [
    path('', views.index, name='index'),
]
