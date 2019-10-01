from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from homepage import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('python-canarias-admin-zone/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('django-rq/', include('django_rq.urls')),
    path('events/', include('events.urls', namespace='events')),
    path('about/', include('about.urls', namespace='about')),
    path('legal/', include('legal.urls', namespace='legal')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
