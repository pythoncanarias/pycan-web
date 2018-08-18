from django.db import models
from apps.events.models import Event


class Tag(models.Model):
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)

    def __str__(self):
        return self.title


class Talk(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)
    description = models.TextField()
    time = models.TimeField()
    tags = models.ManyToManyField(Tag, related_name="talks")

    def __str__(self):
        return self.title


class Abstract(models.Model):
    talk = models.OneToOneField(Talk, on_delete=models.PROTECT)
    description = models.TextField()

    def __str__(self):
        return self.description[:20]


class Speaker(models.Model):
    talk = models.ForeignKey(Talk, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=150)
    name = models.CharField(max_length=220)
    email = models.EmailField(max_length=220, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class Social(models.Model):
    title = models.CharField(max_length=220)
    icon = models.CharField(max_length=220)
    href = models.CharField(max_length=220, help_text="url template, for example: 'mailto:{}' or 'http://t.me/{}'")

    def __str__(self):
        return self.title


class Contact(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT)
    social = models.ForeignKey(Social, on_delete=models.PROTECT)
    value = models.CharField(max_length=220)
