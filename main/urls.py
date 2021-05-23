from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView

from apps.homepage import views

admin_url = 'admin' if settings.DEBUG else 'python-canarias-admin-zone'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path(f'{admin_url}/', admin.site.urls),
    path('api/', include('apps.api.urls', namespace='api')),
    path('django-rq/', include('django_rq.urls')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('legal/', include('apps.legal.urls', namespace='legal')),
    path('members/', include('apps.members.urls', namespace='members')),
    path('jobs/', include('apps.jobs.urls', namespace='jobs')),
]

# redirections
urlpatterns += [
    path(
        'join',
        RedirectView.as_view(url=reverse('members:join')),
        name='goto_join_members',
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
