import locale

from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=220)
    # url of the event is built with: /events/<slug1>/<slug2>/
    slug1 = models.SlugField(max_length=150)
    slug2 = models.SlugField(max_length=150)
    # indicates if the current event is shown in the events page
    active = models.BooleanField(default=False)
    opened_ticket_sales = models.BooleanField(default=False)
    start_date = models.DateField()
    description = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='events/event/',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_long_start_date(self, to_locale=settings.LC_TIME_SPANISH_LOCALE):
        locale.setlocale(locale.LC_TIME, to_locale)
        return self.start_date.strftime('%A %d de %B de %Y').capitalize()
