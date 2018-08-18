from django.db import models
from apps.events.models import Event


class Type(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)

    def __str__(self):
        return self.title


class Sponsorship(models.Model):
    sponsor = models.ForeignKey('Sponsor', on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return "{} {}".format(self.sponsor, self.type)


class Sponsor(models.Model):
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)
    types = models.ManyToManyField(Type, through=Sponsorship)

    def __str__(self):
        return self.title
