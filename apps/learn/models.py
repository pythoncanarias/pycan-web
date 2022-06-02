from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    url = models.URLField(max_length=240)
    labels = models.ManyToManyField(to=Label, related_name='resources')

    def __str__(self):
        return self.name
