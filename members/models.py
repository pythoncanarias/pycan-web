import datetime

from django.contrib.auth.models import User
from django.db import models

from .constants import (
    DEFAULT_MEMBERSHIP_PERIOD,
    DEFAULT_POSITION_PERIOD,
    FEE_AMOUNT,
    FEE_PAYMENT_TYPE,
)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    po_box = models.CharField("Código postal", max_length=10, blank=True)
    city = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_founder = models.BooleanField(default=False)
    is_honorary = models.BooleanField(default=False)
    remarks = models.CharField(max_length=512, blank=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('id', 'user__first_name', 'user__last_name')

    @property
    def active(self):
        last_membership = self.membership_set.last()
        if last_membership is None:
            return False
        valid_until = last_membership.valid_until
        return (valid_until is None or datetime.date.today() <= valid_until)


class Role(models.Model):

    class Meta:
        ordering = ('weight',)

    id = models.CharField(max_length=3, primary_key=True)
    role_name = models.CharField(max_length=120)
    role_desc = models.TextField(blank=True)
    weight = models.IntegerField(
        default=100,
        help_text='Orden relativo a los demas roles. Los más ligeros primero',
    )

    def __str__(self):
        return self.role_name


class Position(models.Model):

    class Meta:
        ordering = ('role__weight',)

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, default='VOC', on_delete=models.PROTECT)
    since = models.DateField()
    until = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=512, blank=True)

    def save(self, *args, **kwargs):
        created = not self.id
        if self.until is None:
            # set 4 years period for the position
            self.until = self.since + datetime.timedelta(
                days=DEFAULT_POSITION_PERIOD)
        super().save(*args, **kwargs)
        if created:
            Position.objects.filter(position=self.position).exclude(
                id=self.id).update(until=self.since)

    def __str__(self):
        return f'{self.member.full_name} as {self.role}'

    @property
    def active(self):
        return (self.until is None or datetime.date.today() <= self.until)

    @classmethod
    def get_current_board(cls):
        """Returns the current governing board.
        """
        today = datetime.date.today()
        return (
            cls.objects
            .select_related('role')
            .select_related('member')
            .select_related('member__user')
            .filter(since__lte=today)
            .filter(models.Q(until__gt=today) | models.Q(until__isnull=True))
            .order_by('role__weight')
        )


class Membership(models.Model):

    class Meta:
        ordering = ('valid_from', 'member')

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    fee_received_at = models.DateField(blank=True, null=True)
    fee_amount = models.IntegerField(choices=FEE_AMOUNT.CHOICES,
                                     default=FEE_AMOUNT.GENERAL)
    fee_payment_type = models.CharField(
        max_length=2,
        choices=FEE_PAYMENT_TYPE.CHOICES,
        default=FEE_PAYMENT_TYPE.BANK_TRANSFERENCE,
        blank=True)
    fee_payment_reference = models.CharField(max_length=128, blank=True)
    remarks = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.member.full_name} from {self.valid_from}'

    def save(self, *args, **kwargs):
        if self.valid_until is None:
            self.valid_until = self.valid_from + datetime.timedelta(
                days=DEFAULT_MEMBERSHIP_PERIOD)
        super().save(args, kwargs)
