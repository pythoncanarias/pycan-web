from django.db import models
from locations.models import Location


class Track(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='tracks'
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class TalkTag(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.title


class TalkLevel(models.Model):
    title = models.CharField(max_length=220)
    order = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.title


class Talk(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        related_name='talks'
    )
    title = models.CharField(max_length=220)
    in_english = models.BooleanField(default=False)
    keynote = models.BooleanField(default=False)
    # duration in minutes
    duration = models.PositiveSmallIntegerField()
    when = models.DateTimeField(blank=True)
    slug = models.SlugField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(
        TalkTag,
        related_name='talks',
        blank=True
    )
    level = models.ForeignKey(
        TalkLevel,
        on_delete=models.PROTECT,
        related_name='talks',
        blank=True
    )
    repo = models.URLField(blank=True)
    slides = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Speaker(models.Model):
    talk = models.ForeignKey(
        Talk,
        on_delete=models.PROTECT,
        related_name='speakers'
    )
    name = models.CharField(max_length=220)
    surname = models.CharField(max_length=220)
    slug = models.SlugField(max_length=150, blank=True)
    email = models.EmailField(max_length=220, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='events/talks/speaker/',
        blank=True
    )
    organization = models.CharField(max_length=220, blank=True)
    position = models.CharField(max_length=220, blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    medium = models.URLField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)
