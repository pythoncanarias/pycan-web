from django.db import models
from events.models import Event

# Nomenclature of classes based on https://goo.gl/2B5Q4U


class Venue(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='venues'
    )
    title = models.CharField(max_length=220)
    address = models.CharField(max_length=220)
    # FIXME from django.contrib.gis.db.models import PointField
    # (but we need postgresql)
    latitude = models.FloatField()
    longitude = models.FloatField()
    slug = models.SlugField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='events/locations/venue/',
        blank=True
    )

    def __str__(self):
        return self.title


class Location(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name='locations'
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveSmallIntegerField(blank=True, null=True)
    # indications of how to reach(arrive) the location
    how_to_reach = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='events/locations/location/',
        blank=True
    )

    def __str__(self):
        return self.title
