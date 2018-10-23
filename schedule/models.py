from django.db import models

from commons.constants import PRIORITY


class SlotCategory(models.Model):
    # Workshop, Talk, Organization, Coffee, Meal, ...
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'slot categories'


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
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(
        SlotTag,
        related_name='slots',
        blank=True
    )

    def __str__(self):
        return self.name

    def get_tags(self):
        return [
            t.slug
            for t in self.tags.all().order_by('slug')
            ]



class Track(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def schedule_in_range(self, start=None, end=None):
        if start and end:
            schedule = self.schedule.filter(start__gte=start, end__lte=end)
        elif start and not end:
            schedule = self.schedule.filter(start__gte=start)
        elif not start and end:
            schedule = self.schedule.filter(end__lte=end)
        else:
            schedule = self.schedule.all()
        return schedule.order_by('start')

    def get_talks(self):
        return [
                {
                'name': _.slot.name,
                'start': _.start.strftime('%H:%M'),
                'end': _.end.strftime('%H:%M'),
                'description': _.slot.description,
                'tags': _.slot.get_tags(),
                'language': _.language,
                }
                for _ in self.schedule.all().select_related('slot').order_by('start')
            ]


class Schedule(models.Model):
    SPANISH = 'ES'
    ENGLISH = 'EN'
    LANGUAGE_CHOICES = (
        (SPANISH, 'Español'),
        (ENGLISH, 'Inglés')
    )

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='schedule'
    )
    location = models.ForeignKey(
        'locations.Location',
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
    speakers = models.ManyToManyField(
        'speakers.Speaker',
        related_name='schedule',
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
        return "{} {}-{}".format(
            self.start.date(),
            self.start.time(),
            self.end.time()
        )

    @property
    def size_for_display(self):
        t = round((self.end - self.start) / self.event.default_slot_duration)
        return t if t > 0 else 1

    @property
    def when_for_display(self):
        return '{} - {}'.format(
            self.start.strftime('%H:%M'),
            self.end.strftime('%H:%M')
        )
