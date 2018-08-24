from django.db import models
from events.models import Event
from commons.constants import PRIORITY


class Organization(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(
        upload_to='organizations/sponsor/',
    )
    url = models.URLField()
    email = models.EmailField(blank=True)
    management_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class OrganizationSubcategory(models.Model):
    # Jade, Zafiro, Diamante, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    code = models.CharField(max_length=16, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='organizations/group/',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "organization subcategories"


class OrganizationCategory(models.Model):
    # Sponsor, Collaborator, Organizer, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    code = models.CharField(max_length=16, unique=True)
    subcategory = models.ForeignKey(
        OrganizationSubcategory,
        on_delete=models.PROTECT,
        related_name='organization_categories',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "organization categories"


class Membership(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='memberships'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='memberships'
    )
    category = models.ForeignKey(
        OrganizationCategory,
        on_delete=models.PROTECT,
        related_name='memberships'
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )

    def __str__(self):
        return self.amount
