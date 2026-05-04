#!/usr/bin/env python

from urllib.parse import quote

from django.templatetags.static import static
from django.db import models

# Nomenclature of classes based on https://goo.gl/2B5Q4U


class Venue(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    address = models.CharField(
        max_length=256, blank=True, help_text='Leave empty for an online event'
    )
    description = models.TextField(blank=True)
    # FIXME from django.contrib.gis.db.models import PointField
    # (but we need postgresql)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    photo = models.ImageField(upload_to='locations/venue/', blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return static('locations/img/noplace.png')

    @property
    def is_online(self):
        return self.address == ''

    def url_google__directions(self):
        return(
            'https://www.google.com/maps/dir/?api=1'
            f'&destination={quote(self.name)}'
            f'/@{self.latitude},{self.longitude}'
            )

class Location(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.PROTECT, related_name='locations'
    )
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    capacity = models.PositiveSmallIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='locations/location/', blank=True)

    def __str__(self):
        return self.name
