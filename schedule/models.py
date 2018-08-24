from django.db import models

from locations.models import Location
from events.models import Event
from speakers.models import Speaker


class SlotCategory(models.Model):
    # Workshop, Talk, Organization, Coffee, Meal, ...
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=16, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SlotTag(models.Model):
    # Machine Learning, Science, DevOps, ...
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SlotLevel(models.Model):
    # Basic, Intermediate, Advanced, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    repo = models.URLField(blank=True)
    slides = models.URLField(blank=True)
    category = models.ForeignKey(
        SlotCategory,
        on_delete=models.PROTECT,
        related_name='slots'
    )
    level = models.ForeignKey(
        SlotLevel,
        on_delete=models.PROTECT,
        related_name='slots',
        blank=True
    )
    tags = models.ManyToManyField(
        SlotTag,
        on_delete=models.PROTECT,
        related_name='slots',
        blank=True
    )

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    SPANISH = 'ES'
    ENGLISH = 'EN'
    LANGUAGE_CHOICES = (
        (SPANISH, 'Español'),
        (ENGLISH, 'Inglés')
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='schedule'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='schedule'
    )
    # if track is null the slot is plenary
    track = models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        related_name='schedule',
        null=True,
        blank=True
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.PROTECT,
        related_name='schedule',
        null=True,
        blank=True
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.PROTECT,
        related_name='schedule'
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=SPANISH
    )

    def __str__(self):
        return self.start
