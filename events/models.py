import locale

from django.db import models
from django.conf import settings

from speakers.models import Speaker
import organizations


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

    @property
    def speakers(self):
        speaker_ids = self.schedule.values_list('speaker').distinct()
        return Speaker.objects.filter(pk__in=speaker_ids)\
            .order_by('name', 'surname')

    @property
    def venue(self):
        return self.schedule.filter(location__isnull=False).\
            first().location.venue

    @property
    def organization_roles(self):
        org_roles_ids = self.memberships.values_list(
            'category__role').distinct()
        org_roles = organizations.models.OrganizationRole.objects.filter(
            pk__in=org_roles_ids).order_by('order')
        return org_roles

    @property
    def memberships_for_display(self):
        result = {}
        for role in self.organization_roles:
            r = {}
            org_categories = organizations.models.OrganizationCategory.\
                objects.filter(role=role).order_by('order')
            for cat in org_categories:
                orgs = []
                memberships = self.memberships.filter(category=cat).order_by(
                    '-amount', 'order', 'organization__name')
                orgs = [m.organization for m in memberships.filter(
                    joint_organization__isnull=True)]
                # insert joint organizations next to its reference
                for i, org in enumerate(orgs):
                    joint_orgs = [
                        o.organization for o in org.joint_memberships.all().
                        order_by('-amount', 'order', 'organization__name')
                    ]
                    for jorg in reversed(joint_orgs):
                        orgs.insert(i + 1, jorg)
                r[cat] = orgs
            result[role] = r
        return result
