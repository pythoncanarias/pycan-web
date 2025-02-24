from django.urls import path

from . import views


app_name = 'certificates'

# http://pythoncanarias.es/certificate/171b89b3-eb00-46f9-af78-f11f7919e5b4.pdf
urlpatterns = [
    path('<uuid:uuid>.pdf', views.download_certificate, name='download'),
    ]
