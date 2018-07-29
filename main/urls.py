from django.contrib import admin
from django.urls import path, include
from apps.homepage import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('events/', include('apps.events.urls', namespace='events')),
]
