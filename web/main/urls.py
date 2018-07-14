from django.contrib import admin
from django.urls import path, include
from homepage import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls', namespace='events')),
]
