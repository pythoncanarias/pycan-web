from django.db import models
from events.models import Event


class SponsorshipLevel(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='sponsorship_levels'
    )
    title = models.CharField(max_length=220)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Sponsor(models.Model):
    title = models.CharField(max_length=220)
    sponsorship_level = models.ForeignKey(
        SponsorshipLevel,
        on_delete=models.PROTECT,
        related_name='sponsors'
    )
    slug = models.SlugField(max_length=150, blank=True)
    logo = models.ImageField(
        upload_to='events/sponsors/sponsor/',
        blank=True
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
