from django.db import models

from apps.commons.constants import PRIORITY


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

    class Meta:
        ordering = ['name']


class SlotLevel(models.Model):
    # Basic, Intermediate, Advanced, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM,
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
        related_name='slots',
    )
    level = models.ForeignKey(
        SlotLevel,
        on_delete=models.PROTECT,
        related_name='slots',
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(SlotTag, related_name='slots', blank=True)

    def __str__(self):
        return self.name

    def get_level(self):
        return self.level.name if self.level else 'N/A'

    def get_tags(self):
        return [t.slug for t in self.tags.all().order_by('slug')]

    def is_talk(self):
        return self.category_id in (1, 2)


class Track(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def schedule_in_range(self, start=None, end=None, event=None):
        queryset = self.schedule.all().order_by('start')
        if start:
            queryset = queryset.filter(start__gte=start)
        if end:
            queryset = queryset.filter(end__lte=end)
        if event:
            queryset = queryset.filter(event=event)
        return queryset

    def get_talks(self, event=None):
        qs = self.schedule.select_related('slot')
        if event:
            qs = qs.filter(event=event)
        qs = qs.order_by('start')
        return [{
            'talk_id': t.slot.pk,
            'name': t.slot.name,
            'start': t.start.strftime('%H:%M'),
            'end': t.end.strftime('%H:%M'),
            'description': t.slot.description,
            'tags': t.slot.get_tags(),
            'language': t.language,
            'speakers': t.get_speakers(),
        } for t in qs]


class Schedule(models.Model):
    SPANISH = 'ES'
    ENGLISH = 'EN'
    LANGUAGE_CHOICES = ((SPANISH, 'Español'), (ENGLISH, 'Inglés'))

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='schedule',
    )
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.PROTECT,
        related_name='schedule',
    )
    # if track is null the slot is plenary
    track = models.ForeignKey(
        Track,
        on_delete=models.PROTECT,
        related_name='schedule',
        null=True,
        blank=True,
    )
    speakers = models.ManyToManyField(
        'speakers.Speaker',
        related_name='schedule',
        blank=True,
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.PROTECT,
        related_name='schedule',
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=SPANISH,
    )

    def __str__(self):
        return "{} {}-{}".format(
            self.start.date(),
            self.start.time(),
            self.end.time(),
        )

    def get_speakers(self):
        qs = self.speakers.all().order_by('surname', 'name')
        result = [{
            'speaker_id': speaker.pk,
            'name': speaker.name,
            'surname': speaker.surname,
            'bio': speaker.bio,
            'photo': speaker.photo_url,
            'social': speaker.socials(),
        } for speaker in qs]
        return result

    def size_for_display(self):
        t = round((self.end - self.start) / self.event.default_slot_duration)
        return t if t > 0 else 1

    def track_name(self):
        if self.track:
            return self.track.name
        else:
            return 'No track'
