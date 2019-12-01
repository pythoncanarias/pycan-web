from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from pytz import utc

from .constants import (MEMBER_POSITION, FEE_PAYMENT_TYPE, FEE_AMOUNT,
                        MEMBER_CATEGORY)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    member_until = models.DateTimeField(auto_now_add=True)

    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    po_box = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    @property
    def active(self):
        return datetime.now(tz=utc) < self.member_until

    def __str__(self):
        return (f'{self.user.first_name} {self.user.last_name} '
                'member until {self.member_until}')


class Position(models.Model):
    position = models.IntegerField(choices=MEMBER_POSITION.CHOICES)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)

    since = models.DateField(auto_now_add=True)
    until = models.DateField(blank=True, null=True)

    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        created = not self.id
        super().save(*args, **kwargs)

        if created and self.active:
            Position.objects.filter(
                active=True, position=self.position).update(until=self.since,
                                                            active=False)


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    member_category = models.CharField(max_length=1,
                                       choices=MEMBER_CATEGORY.CHOICES,
                                       default=MEMBER_CATEGORY.NUMBER)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    fee_received_at = models.DateTimeField(blank=True)
    fee_amount = models.FloatField(choices=FEE_AMOUNT.CHOICES,
                                   default=FEE_AMOUNT.GENERAL,
                                   blank=True,
                                   null=True)
    fee_payment_type = models.CharField(
        max_length=2,
        choices=FEE_PAYMENT_TYPE.CHOICES,
        default=FEE_PAYMENT_TYPE.BANK_TRANSFERENCE)
    fee_payment_reference = models.CharField(max_length=128, blank=True)
