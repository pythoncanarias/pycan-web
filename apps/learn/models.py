import re

from django.db import models

from . import colors


class Label(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    # Label color in hex mode
    color = models.CharField(
        max_length=8, default=colors.get_random_hex_color()
    )

    def __str__(self):
        return self.name

    @property
    def foreground_color(self):
        rgb_color = colors.get_rgb_from_hex(self.color)
        luminance = colors.get_luminance(*rgb_color)
        return colors.BLACK if luminance > 128 else colors.WHITE

    def save(self, *args, **kwargs):
        self.color = re.sub(r'^#', '', self.color)
        super().save(*args, **kwargs)


class Resource(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    url = models.URLField(max_length=240)
    labels = models.ManyToManyField(to=Label, related_name='resources')

    def __str__(self):
        return self.name
