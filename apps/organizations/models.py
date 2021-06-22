#!/usr/bin/env python

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save

from apps.commons.constants import PRIORITY


class Organization(models.Model):

    name = models.CharField(max_length=256)
    logo = models.FileField(upload_to='organizations/organization/')
    address = models.CharField(max_length=100, blank=True, null=True)
    rest_address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    cif = models.CharField(max_length=10, blank=True, null=True)
    iban = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    bank = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True)
    paypal_username = models.CharField(max_length=50, blank=True)

    @classmethod
    def load_main_organization(cls):
        key = 'organizations.organization'
        org = cache.get(key)
        if org is None:
            org = Organization.objects.get(
                name__istartswith=settings.ORGANIZATION_NAME
            )
            cache.set(key, org, timeout=604800)  # 7 días
        return org

    @property
    def full_address(self):
        return (
            f'{self.address} {self.rest_address or ""}| '
            f'{self.postal_code} {self.city}'
        )

    def __str__(self):
        return self.name

    def joint_organizations(self):
        return [
            m.organization
            for m in self.joint_memberships.order_by(
                '-_amount', 'order', 'organization__name'
            )
        ]

    @property
    def paypal_me(self):
        return f'https://paypal.me/{self.paypal_username}'

    class Meta:
        ordering = ['name']


def clear_organization_cache(sender, **kwargs):
    """Limpia la cache de la informacion sobre la organizacion.

    Ver commons.content_procesors.main_organization_data.

    Cada vez que se almacene informacion en la tabla de organizaciones,
    se elmimina la cache.
    """
    key = 'organizations.organization'
    cache.delete(key)


post_save.connect(
    clear_organization_cache,
    sender=Organization,
    dispatch_uid="clear_organization_cache",
)


class OrganizationRole(models.Model):
    # Sponsor, Collaborator, Organizer, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM,
    )
    code = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)
    logo = models.FileField(
        upload_to='organizations/organization_role/',
        blank=True,
    )
    display_name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.display_name or self.name


class OrganizationCategory(models.Model):
    # Jade sponsor, Zafiro sponsor, Diamante sponsor, organizer, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM,
    )
    code = models.CharField(max_length=32, unique=True)
    role = models.ForeignKey(
        OrganizationRole,
        on_delete=models.PROTECT,
        related_name='organization_categories',
    )
    description = models.TextField(blank=True)
    display_name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.display_name or self.name

    class Meta:
        verbose_name_plural = "organization categories"

    def organizations(self, event=None, exclude_joint_organizations=True):
        memberships = self.memberships.order_by(
            '-_amount',
            'order',
            'organization__name',
        )
        if event:
            memberships = memberships.filter(event=event)
        if exclude_joint_organizations:
            memberships = memberships.exclude(joint_organization__isnull=False)
        return [m.organization for m in memberships]


class Membership(models.Model):
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='memberships',
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='memberships',
    )
    category = models.ForeignKey(
        OrganizationCategory,
        on_delete=models.PROTECT,
        related_name='memberships',
    )
    _amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM,
    )
    management_email = models.EmailField(
        blank=True,
        help_text='Management email of the organization used during the event',
    )
    joint_organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='joint_memberships',
        help_text='Organizations joint with other organizations',
        blank=True,
        null=True,
    )

    @property
    def amount(self):
        """Return how much funds has the organization provided to the event.

        :return: How much has the organization funded.
        :rtype: Decimal
        """
        invoices = self.event.invoices.for_organization(self.organization)

        if not invoices:
            return self._amount
        return invoices.get().concepts_total

    def __str__(self):
        return "{} {} {}".format(self.organization, self.category, self.amount)

    def get_email(self):
        return self.management_email or self.organization.email
