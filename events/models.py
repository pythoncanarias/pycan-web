import locale
import datetime
import pytz

from django.db import models
from django.conf import settings

from speakers.models import Speaker
from organizations.models import OrganizationRole
from schedule.models import Track


class Event(models.Model):
    name = models.CharField(max_length=256)
    # url of the event is /events/<slug>
    slug = models.SlugField(unique=True)
    active = models.BooleanField(
        help_text='The current event is shown in the events page',
        default=False
    )
    opened_ticket_sales = models.BooleanField(default=False)
    start_date = models.DateField()
    # 50 minutes as default duration for each slot
    default_slot_duration = models.DurationField(default=50 * 60)
    short_description = models.TextField(blank=True)
    description = models.TextField(
        blank=True,
        help_text='Markdown is allowed'
    )
    cover = models.ImageField(
        upload_to='events/event/',
        blank=True
    )
    poster = models.FileField(
        upload_to='events/event/',
        blank=True
    )
    sponsorship_brochure = models.FileField(
        upload_to='events/event/',
        blank=True
    )
    hero = models.ImageField(
        upload_to='events/event/',
        blank=True
    )

    def __str__(self):
        return self.name

    def get_long_start_date(self, to_locale=settings.LC_TIME_SPANISH_LOCALE):
        locale.setlocale(locale.LC_TIME, to_locale)
        return self.start_date.strftime('%A %d de %B de %Y').capitalize()

    def speakers(self):
        speaker_ids = self.schedule.values_list('speakers').distinct()
        return Speaker.objects.filter(pk__in=speaker_ids).\
            order_by('name', 'surname')

    def venue(self):
        return self.schedule.filter(location__isnull=False).\
            first().location.venue

    def organization_roles(self):
        org_roles_ids = self.memberships.values_list(
            'category__role').distinct()
        return OrganizationRole.objects.filter(pk__in=org_roles_ids).\
            order_by('order', 'name')

    def memberships_for_display(self):
        result = {}
        for role in self.organization_roles():
            r = {}
            for cat in role.organization_categories.order_by('order', 'name'):
                orgs = cat.organizations()
                # insert joint organizations next to its reference
                for i, org in enumerate(orgs):
                    for jorg in reversed(org.joint_organizations()):
                        orgs.insert(i + 1, jorg)
                if orgs:
                    r[cat] = orgs
            if r:
                result[role] = r
        return result

    def tracks(self):
        tracks_ids = self.schedule.values_list('track').distinct()
        return Track.objects.filter(pk__in=tracks_ids).\
            order_by('order', 'name')

    def plenary_scheduled_items(self):
        return self.schedule.filter(track__isnull=True).order_by('start')

    @property
    def start_date_as_datetime(self):
        return datetime.datetime.combine(
            self.start_date, datetime.time(0, 0, tzinfo=pytz.UTC))

    def _scheduled_items_for_display(self, start=None, end=None):
        result = {'type': 'scheduled_items', 'tracks': []}
        exist_scheduled_item = False
        for track in self.tracks():
            scheduled_items = track.schedule_in_range(start, end)
            if scheduled_items:
                exist_scheduled_item = True
            result['tracks'].append(
                {'track': track, 'scheduled_items': scheduled_items})
        if not exist_scheduled_item:
            result = None
        return result

    def schedule_for_display(self):
        result = [{'type': 'tracks', 'tracks': self.tracks()}]
        start, end = self.start_date_as_datetime, None
        for psi in list(self.plenary_scheduled_items()):
            end = psi.start
            scheduled_items = self._scheduled_items_for_display(start, end)
            if scheduled_items:
                result.append(scheduled_items)
            result.append({'type': 'plenary_scheduled_item', 'schedule': psi})
            start, end = psi.end, None

        scheduled_items = self._scheduled_items_for_display(start, end)
        if scheduled_items:
            result.append(scheduled_items)

        return result
