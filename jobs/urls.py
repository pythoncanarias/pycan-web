from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.list_active_job_offers, name='index'),
]
