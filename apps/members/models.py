import datetime

from django.contrib.auth.models import User
from django.db import models

from .constants import (DEFAULT_MEMBERSHIP_PERIOD, DEFAULT_POSITION_PERIOD,
                        FEE_AMOUNT, FEE_PAYMENT_TYPE, MEMBER_POSITION)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    po_box = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_founder = models.BooleanField(default=False)
    is_honorary = models.BooleanField(default=False)
    remarks = models.CharField(max_length=512, blank=True)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def member_id(self):
        return self.id

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


class Position(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    position = models.CharField(max_length=3, choices=MEMBER_POSITION.CHOICES)
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
        return f'{self.member.full_name} as {self.position}'

    class Meta:
        ordering = ('since', 'position', 'member')

    @property
    def active(self):
        return (self.until is None or datetime.date.today() <= self.until)


class Membership(models.Model):
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

    class Meta:
        ordering = ('valid_from', 'member')

    def save(self, *args, **kwargs):
        if self.valid_until is None:
            self.valid_until = self.valid_from + datetime.timedelta(
                days=DEFAULT_MEMBERSHIP_PERIOD)
        super().save(args, kwargs)
