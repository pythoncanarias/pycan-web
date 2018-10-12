from django.db import models

from commons.constants import PRIORITY


class Organization(models.Model):
    name = models.CharField(max_length=256)
    logo = models.FileField(upload_to='organizations/organization/')
    url = models.URLField()
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    def joint_organizations(self):
        return [
            m.organization for m in self.joint_memberships.
            order_by('-amount', 'order', 'organization__name')
        ]


class OrganizationRole(models.Model):
    # Sponsor, Collaborator, Organizer, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    code = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)
    logo = models.FileField(
        upload_to='organizations/organization_role/',
        blank=True
    )
    display_name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.display_name or self.name


class OrganizationCategory(models.Model):
    # Jade sponsor, Zafiro sponsor, Diamante sponsor, organizer, ...
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField(
        choices=PRIORITY.CHOICES,
        default=PRIORITY.MEDIUM
    )
    code = models.CharField(max_length=32, unique=True)
    role = models.ForeignKey(
        OrganizationRole,
        on_delete=models.PROTECT,
        related_name='organization_categories'
    )
    description = models.TextField(blank=True)
    display_name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.display_name or self.name

    class Meta:
        verbose_name_plural = "organization categories"

    def organizations(self, exclude_joint_organizations=True):
        memberships = self.memberships.order_by(
            '-amount', 'order', 'organization__name')
        if exclude_joint_organizations:
            memberships = memberships.exclude(joint_organization__isnull=False)
        return [m.organization for m in memberships]


class Membership(models.Model):
    event = models.ForeignKey(
        'events.Event',
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
    management_email = models.EmailField(
        blank=True,
        help_text='Management email of the organization used during the event'
    )
    joint_organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='joint_memberships',
        help_text='Organizations joint with other organizations',
        blank=True,
        null=True
    )

    def __str__(self):
        return "{} {} {}".format(self.organization, self.category, self.amount)

    def get_email(self):
        return self.management_email or self.organization.email
