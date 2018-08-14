from django.db import models
from apps.events.models import Event


class Location(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)
    description = models.TextField()
    address = models.CharField(max_length=220)
    # FIXME from django.contrib.gis.db.models import PointField (but we need postgresql)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title
